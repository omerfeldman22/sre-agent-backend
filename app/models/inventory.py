from pydantic import BaseModel


class InventoryItem(BaseModel):
    id: str
    productId: str
    productName: str
    category: str
    currentStock: int
    reservedStock: int
    availableStock: int
    reorderLevel: int
    lastRestocked: str
