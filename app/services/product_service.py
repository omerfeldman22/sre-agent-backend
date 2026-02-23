"""Product service — business logic around the product catalog."""

from __future__ import annotations

import logging
from math import ceil

from app.models import Product
from app.models.common import PaginatedResponse
from app.data.store import PRODUCTS

logger = logging.getLogger(__name__)


def list_products(
    search: str | None = None,
    category: str | None = None,
    page: int = 1,
    pageSize: int = 12,
) -> PaginatedResponse[Product]:
    """Return a filtered, paginated list of products."""
    items = list(PRODUCTS.values())

    if search:
        q = search.lower()
        items = [
            p
            for p in items
            if q in p.name.lower() or q in p.description.lower()
        ]

    if category:
        items = [p for p in items if p.category == category]

    total = len(items)
    total_pages = max(1, ceil(total / pageSize))
    start = (page - 1) * pageSize
    end = start + pageSize

    logger.info(
        "list_products search=%s category=%s page=%d total=%d",
        search,
        category,
        page,
        total,
    )

    return PaginatedResponse[Product](
        items=items[start:end],
        total=total,
        page=page,
        pageSize=pageSize,
        totalPages=total_pages,
    )


def get_product(product_id: str) -> Product | None:
    """Return a single product by ID, or None if not found."""
    return PRODUCTS.get(product_id)


def get_categories() -> list[str]:
    """Return a sorted, deduplicated list of product categories."""
    return sorted({p.category for p in PRODUCTS.values()})
