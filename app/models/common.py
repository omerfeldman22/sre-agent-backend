from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    pageSize: int
    totalPages: int


class ApiErrorResponse(BaseModel):
    message: str
    statusCode: int
    details: str | None = None
