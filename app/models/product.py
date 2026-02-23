from datetime import datetime
from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    category: str
    imageUrl: str
    stock: int
    createdAt: str
    updatedAt: str
