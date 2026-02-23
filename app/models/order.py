from enum import Enum
from pydantic import BaseModel, EmailStr


class OrderStatus(str, Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    FAILED = "Failed"


class OrderItem(BaseModel):
    id: str
    productId: str
    productName: str
    quantity: int
    unitPrice: float
    totalPrice: float


class OrderStatusChange(BaseModel):
    status: OrderStatus
    timestamp: str
    note: str | None = None


class Order(BaseModel):
    id: str
    customerName: str
    customerEmail: str
    status: OrderStatus
    items: list[OrderItem]
    totalAmount: float
    statusHistory: list[OrderStatusChange]
    createdAt: str
    updatedAt: str


class CreateOrderItemRequest(BaseModel):
    productId: str
    quantity: int


class CreateOrderRequest(BaseModel):
    customerName: str
    customerEmail: EmailStr
    items: list[CreateOrderItemRequest]


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus
    note: str | None = None
