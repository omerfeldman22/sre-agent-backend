"""Product endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.models import Product
from app.models.common import PaginatedResponse
from app.services import product_service

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/categories", response_model=list[str])
async def get_categories():
    """Return all available product categories."""
    return product_service.get_categories()


@router.get("", response_model=PaginatedResponse[Product])
async def list_products(
    search: str | None = Query(None, description="Search term for name/description"),
    category: str | None = Query(None, description="Filter by category"),
    page: int = Query(1, ge=1, description="Page number"),
    pageSize: int = Query(12, ge=1, le=100, description="Items per page"),
):
    """Return a paginated list of products."""
    return product_service.list_products(
        search=search, category=category, page=page, pageSize=pageSize
    )


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Return a product by ID."""
    product = product_service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
