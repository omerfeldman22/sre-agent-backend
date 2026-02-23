"""Order endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.models import (
    Order,
    OrderStatus,
    CreateOrderRequest,
    UpdateOrderStatusRequest,
)
from app.models.common import PaginatedResponse
from app.services import order_service

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.get("", response_model=PaginatedResponse[Order])
async def list_orders(
    status: OrderStatus | None = Query(None, description="Filter by order status"),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(10, ge=1, le=100, description="Items per page"),
):
    """Return a paginated list of orders."""
    return order_service.list_orders(status=status, page=page, pageSize=pageSize)


@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Return an order by ID."""
    order = order_service.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=Order, status_code=201)
async def create_order(request: CreateOrderRequest):
    """Create a new order."""
    try:
        return order_service.create_order(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{order_id}/status", response_model=Order)
async def update_order_status(order_id: str, body: UpdateOrderStatusRequest):
    """Update the status of an order."""
    order = order_service.update_order_status(
        order_id=order_id,
        status=body.status,
        note=body.note,
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
