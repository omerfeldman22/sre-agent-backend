"""Inventory endpoints."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.models import InventoryItem
from app.services import inventory_service

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("", response_model=list[InventoryItem])
async def list_inventory():
    """Return all inventory items."""
    return inventory_service.list_inventory()


@router.get("/{product_id}", response_model=InventoryItem)
async def get_inventory_by_product(product_id: str):
    """Return inventory for a specific product."""
    item = inventory_service.get_inventory_by_product(product_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Inventory not found for this product")
    return item
