"""In-memory data store with realistic seed data for the SRE demo."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from copy import deepcopy

from app.models import (
    Product,
    Order,
    OrderItem,
    OrderStatus,
    OrderStatusChange,
    InventoryItem,
)

# ─── Helpers ──────────────────────────────────────────────────────────────────

_now = datetime.now(timezone.utc)


def _ts(days_ago: int = 0, hours_ago: int = 0) -> str:
    """Return an ISO-8601 timestamp offset from 'now'."""
    return (_now - timedelta(days=days_ago, hours=hours_ago)).isoformat()


def _uid() -> str:
    return str(uuid.uuid4())


# Deterministic UUIDs so every pod has identical data
_PRODUCT_IDS = [
    "a1b2c3d4-1111-4000-8000-000000000001",
    "a1b2c3d4-1111-4000-8000-000000000002",
    "a1b2c3d4-1111-4000-8000-000000000003",
    "a1b2c3d4-1111-4000-8000-000000000004",
    "a1b2c3d4-1111-4000-8000-000000000005",
    "a1b2c3d4-1111-4000-8000-000000000006",
    "a1b2c3d4-1111-4000-8000-000000000007",
    "a1b2c3d4-1111-4000-8000-000000000008",
    "a1b2c3d4-1111-4000-8000-000000000009",
    "a1b2c3d4-1111-4000-8000-00000000000a",
    "a1b2c3d4-1111-4000-8000-00000000000b",
    "a1b2c3d4-1111-4000-8000-00000000000c",
    "a1b2c3d4-1111-4000-8000-00000000000d",
    "a1b2c3d4-1111-4000-8000-00000000000e",
    "a1b2c3d4-1111-4000-8000-00000000000f",
]

_ORDER_IDS = [
    "b2c3d4e5-2222-4000-8000-000000000001",
    "b2c3d4e5-2222-4000-8000-000000000002",
    "b2c3d4e5-2222-4000-8000-000000000003",
    "b2c3d4e5-2222-4000-8000-000000000004",
    "b2c3d4e5-2222-4000-8000-000000000005",
    "b2c3d4e5-2222-4000-8000-000000000006",
    "b2c3d4e5-2222-4000-8000-000000000007",
    "b2c3d4e5-2222-4000-8000-000000000008",
]

_ORDER_ITEM_IDS = [
    "c3d4e5f6-3333-4000-8000-{:012d}".format(i) for i in range(1, 30)
]

_INVENTORY_IDS = [
    "d4e5f6a7-4444-4000-8000-{:012d}".format(i) for i in range(1, 20)
]

_order_item_counter = 0


def _next_order_item_id() -> str:
    global _order_item_counter
    uid = _ORDER_ITEM_IDS[_order_item_counter]
    _order_item_counter += 1
    return uid


# ─── Seed Products ───────────────────────────────────────────────────────────

PRODUCTS: dict[str, Product] = {}

_product_seed = [
    {
        "name": "Wireless Bluetooth Headphones",
        "description": "Premium noise-cancelling over-ear headphones with 30-hour battery life and Hi-Res audio support.",
        "price": 149.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
        "stock": 85,
    },
    {
        "name": "Mechanical Keyboard RGB",
        "description": "Full-size mechanical keyboard with Cherry MX switches, per-key RGB lighting, and USB-C connectivity.",
        "price": 129.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=400",
        "stock": 42,
    },
    {
        "name": "Ergonomic Office Chair",
        "description": "Adjustable lumbar support mesh chair with headrest, armrests, and 360-degree swivel base.",
        "price": 399.99,
        "category": "Furniture",
        "imageUrl": "https://images.unsplash.com/photo-1592078615290-033ee584e267?w=400",
        "stock": 15,
    },
    {
        "name": "Standing Desk Converter",
        "description": "Height-adjustable sit-stand desk riser with dual monitor support and keyboard tray.",
        "price": 279.99,
        "category": "Furniture",
        "imageUrl": "https://images.unsplash.com/photo-1611269154421-4e27233ac5c7?w=400",
        "stock": 23,
    },
    {
        "name": "4K Ultra HD Monitor 27\"",
        "description": "27-inch IPS panel with HDR400, 99% sRGB color accuracy, and USB-C power delivery.",
        "price": 449.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400",
        "stock": 31,
    },
    {
        "name": "Laptop Backpack",
        "description": "Water-resistant 17-inch laptop backpack with USB charging port and anti-theft design.",
        "price": 59.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400",
        "stock": 120,
    },
    {
        "name": "Wireless Mouse Pro",
        "description": "Ergonomic wireless mouse with 16000 DPI sensor, programmable buttons, and dual connectivity.",
        "price": 69.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400",
        "stock": 95,
    },
    {
        "name": "USB-C Hub 7-in-1",
        "description": "Multiport adapter with HDMI 4K, USB 3.0, SD card reader, and 100W PD charging.",
        "price": 49.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400",
        "stock": 67,
    },
    {
        "name": "Desk Lamp LED",
        "description": "Adjustable LED desk lamp with 5 color temperatures, USB charging port, and touch controls.",
        "price": 34.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=400",
        "stock": 54,
    },
    {
        "name": "Webcam 1080p",
        "description": "Full HD webcam with auto-focus, built-in microphone, and adjustable mounting clip.",
        "price": 79.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400",
        "stock": 38,
    },
    {
        "name": "Noise Machine White",
        "description": "Portable white noise machine with 20 soothing sounds and programmable sleep timer.",
        "price": 29.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1558618666-fcd25c85f82e?w=400",
        "stock": 73,
    },
    {
        "name": "Cable Management Kit",
        "description": "Complete cable organiser set with clips, sleeves, and adhesive cord holders.",
        "price": 19.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1601524909162-ae8725290836?w=400",
        "stock": 150,
    },
    {
        "name": "Bookshelf 5-Tier",
        "description": "Modern industrial bookshelf with steel frame and rustic wood shelves.",
        "price": 189.99,
        "category": "Furniture",
        "imageUrl": "https://images.unsplash.com/photo-1594620302200-9a762244a156?w=400",
        "stock": 8,
    },
    {
        "name": "Portable SSD 1TB",
        "description": "Compact external SSD with 1050 MB/s read speed, USB 3.2, and shock-resistant casing.",
        "price": 109.99,
        "category": "Electronics",
        "imageUrl": "https://images.unsplash.com/photo-1531492746076-161ca9bcad09?w=400",
        "stock": 45,
    },
    {
        "name": "Monitor Arm Mount",
        "description": "Gas spring single monitor arm supporting up to 32-inch displays with full motion adjustment.",
        "price": 89.99,
        "category": "Accessories",
        "imageUrl": "https://images.unsplash.com/photo-1616763355548-1b11cea702ee?w=400",
        "stock": 3,
    },
]

for i, p in enumerate(_product_seed):
    pid = _PRODUCT_IDS[i]
    PRODUCTS[pid] = Product(
        id=pid,
        createdAt=_ts(days_ago=90 - i * 5),
        updatedAt=_ts(days_ago=max(0, 10 - i)),
        **p,
    )

_product_ids = list(PRODUCTS.keys())

# ─── Seed Orders ─────────────────────────────────────────────────────────────

ORDERS: dict[str, Order] = {}

_order_seed = [
    {
        "customerName": "Alice Johnson",
        "customerEmail": "alice.johnson@example.com",
        "status": OrderStatus.DELIVERED,
        "items_idx": [0, 5],
        "quantities": [1, 2],
        "days_ago": 14,
    },
    {
        "customerName": "Bob Smith",
        "customerEmail": "bob.smith@example.com",
        "status": OrderStatus.SHIPPED,
        "items_idx": [1, 7],
        "quantities": [1, 1],
        "days_ago": 7,
    },
    {
        "customerName": "Carol Davis",
        "customerEmail": "carol.davis@example.com",
        "status": OrderStatus.PROCESSING,
        "items_idx": [2],
        "quantities": [1],
        "days_ago": 3,
    },
    {
        "customerName": "David Lee",
        "customerEmail": "david.lee@example.com",
        "status": OrderStatus.PENDING,
        "items_idx": [4, 6, 8],
        "quantities": [1, 1, 2],
        "days_ago": 1,
    },
    {
        "customerName": "Eva Martinez",
        "customerEmail": "eva.martinez@example.com",
        "status": OrderStatus.FAILED,
        "items_idx": [3],
        "quantities": [1],
        "days_ago": 10,
    },
    {
        "customerName": "Frank Wilson",
        "customerEmail": "frank.wilson@example.com",
        "status": OrderStatus.DELIVERED,
        "items_idx": [9, 10, 11],
        "quantities": [2, 1, 3],
        "days_ago": 21,
    },
    {
        "customerName": "Grace Chen",
        "customerEmail": "grace.chen@example.com",
        "status": OrderStatus.SHIPPED,
        "items_idx": [13],
        "quantities": [2],
        "days_ago": 5,
    },
    {
        "customerName": "Henry Brown",
        "customerEmail": "henry.brown@example.com",
        "status": OrderStatus.PROCESSING,
        "items_idx": [12, 14],
        "quantities": [1, 1],
        "days_ago": 2,
    },
]

# Status progression for building realistic history
_STATUS_FLOW: dict[OrderStatus, list[OrderStatus]] = {
    OrderStatus.PENDING: [OrderStatus.PENDING],
    OrderStatus.PROCESSING: [OrderStatus.PENDING, OrderStatus.PROCESSING],
    OrderStatus.SHIPPED: [
        OrderStatus.PENDING,
        OrderStatus.PROCESSING,
        OrderStatus.SHIPPED,
    ],
    OrderStatus.DELIVERED: [
        OrderStatus.PENDING,
        OrderStatus.PROCESSING,
        OrderStatus.SHIPPED,
        OrderStatus.DELIVERED,
    ],
    OrderStatus.FAILED: [OrderStatus.PENDING, OrderStatus.FAILED],
}

for oi, o in enumerate(_order_seed):
    oid = _ORDER_IDS[oi]
    product_indices: list[int] = o["items_idx"]  # type: ignore[assignment]
    quantities: list[int] = o["quantities"]  # type: ignore[assignment]
    days_ago: int = o["days_ago"]  # type: ignore[assignment]
    status: OrderStatus = o["status"]  # type: ignore[assignment]

    items: list[OrderItem] = []
    total_amount = 0.0
    for idx, qty in zip(product_indices, quantities):
        product = PRODUCTS[_product_ids[idx]]
        item_total = product.price * qty
        total_amount += item_total
        items.append(
            OrderItem(
                id=_next_order_item_id(),
                productId=product.id,
                productName=product.name,
                quantity=qty,
                unitPrice=product.price,
                totalPrice=round(item_total, 2),
            )
        )

    # Build status history
    history: list[OrderStatusChange] = []
    flow = _STATUS_FLOW[status]
    for i, s in enumerate(flow):
        history.append(
            OrderStatusChange(
                status=s,
                timestamp=_ts(days_ago=days_ago - i, hours_ago=0),
                note=f"Order {s.value.lower()}" if i > 0 else "Order placed",
            )
        )

    ORDERS[oid] = Order(
        id=oid,
        customerName=o["customerName"],  # type: ignore[arg-type]
        customerEmail=o["customerEmail"],  # type: ignore[arg-type]
        status=status,
        items=items,
        totalAmount=round(total_amount, 2),
        statusHistory=history,
        createdAt=_ts(days_ago=days_ago),
        updatedAt=_ts(days_ago=max(0, days_ago - len(flow) + 1)),
    )

# ─── Seed Inventory ──────────────────────────────────────────────────────────

INVENTORY: dict[str, InventoryItem] = {}

for inv_i, (pid, product) in enumerate(PRODUCTS.items()):
    reserved = min(product.stock // 5, 10)
    inv_id = _INVENTORY_IDS[inv_i]
    INVENTORY[pid] = InventoryItem(
        id=inv_id,
        productId=pid,
        productName=product.name,
        category=product.category,
        currentStock=product.stock,
        reservedStock=reserved,
        availableStock=product.stock - reserved,
        reorderLevel=max(5, product.stock // 4),
        lastRestocked=_ts(days_ago=max(1, product.stock % 15)),
    )
