"""Inventory service — business logic around inventory management."""

from __future__ import annotations

import logging

from app.models import InventoryItem
from app.data.store import INVENTORY

logger = logging.getLogger(__name__)


def list_inventory() -> list[InventoryItem]:
    """Return the full inventory list."""
    items = list(INVENTORY.values())
    logger.info("list_inventory count=%d", len(items))
    return items


def get_inventory_by_product(product_id: str) -> InventoryItem | None:
    """Return inventory for a specific product, or None if not found."""
    return INVENTORY.get(product_id)
