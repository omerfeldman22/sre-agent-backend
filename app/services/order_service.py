"""Order service — business logic around orders."""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from math import ceil

from app.models import (
    Order,
    OrderItem,
    OrderStatus,
    OrderStatusChange,
    CreateOrderRequest,
)
from app.models.common import PaginatedResponse
from app.data.store import ORDERS, PRODUCTS

logger = logging.getLogger(__name__)


def list_orders(
    status: OrderStatus | None = None,
    page: int = 1,
    pageSize: int = 10,
) -> PaginatedResponse[Order]:
    """Return a filtered, paginated list of orders."""
    items = list(ORDERS.values())

    if status:
        items = [o for o in items if o.status == status]

    # Sort newest first
    items.sort(key=lambda o: o.createdAt, reverse=True)

    total = len(items)
    total_pages = max(1, ceil(total / pageSize))
    start = (page - 1) * pageSize
    end = start + pageSize

    logger.info(
        "list_orders status=%s page=%d total=%d", status, page, total
    )

    return PaginatedResponse[Order](
        items=items[start:end],
        total=total,
        page=page,
        pageSize=pageSize,
        totalPages=total_pages,
    )


def get_order(order_id: str) -> Order | None:
    """Return a single order by ID, or None if not found."""
    return ORDERS.get(order_id)


def create_order(request: CreateOrderRequest) -> Order:
    """Create a new order from the given request.

    Raises ValueError if any referenced product does not exist.
    """
    now = datetime.now(timezone.utc).isoformat()
    items: list[OrderItem] = []
    total_amount = 0.0

    for item_req in request.items:
        product = PRODUCTS.get(item_req.productId)
        if product is None:
            raise ValueError(f"Product {item_req.productId} not found")

        item_total = product.price * item_req.quantity
        total_amount += item_total
        items.append(
            OrderItem(
                id=str(uuid.uuid4()),
                productId=product.id,
                productName=product.name,
                quantity=item_req.quantity,
                unitPrice=product.price,
                totalPrice=round(item_total, 2),
            )
        )

    order = Order(
        id=str(uuid.uuid4()),
        customerName=request.customerName,
        customerEmail=request.customerEmail,
        status=OrderStatus.PENDING,
        items=items,
        totalAmount=round(total_amount, 2),
        statusHistory=[
            OrderStatusChange(
                status=OrderStatus.PENDING,
                timestamp=now,
                note="Order placed",
            )
        ],
        createdAt=now,
        updatedAt=now,
    )

    ORDERS[order.id] = order
    logger.info("create_order id=%s total=%.2f", order.id, total_amount)
    return order


def update_order_status(
    order_id: str, status: OrderStatus, note: str | None = None
) -> Order | None:
    """Advance an order to a new status.

    Returns the updated order, or None if not found.
    """
    order = ORDERS.get(order_id)
    if order is None:
        return None

    now = datetime.now(timezone.utc).isoformat()

    # Create a new order with updated status (Pydantic models are immutable by default)
    updated = order.model_copy(
        update={
            "status": status,
            "updatedAt": now,
            "statusHistory": order.statusHistory
            + [
                OrderStatusChange(
                    status=status,
                    timestamp=now,
                    note=note or f"Order {status.value.lower()}",
                )
            ],
        }
    )

    ORDERS[order_id] = updated
    logger.info("update_order_status id=%s status=%s", order_id, status.value)
    return updated
