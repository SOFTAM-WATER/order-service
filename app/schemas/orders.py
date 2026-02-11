import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Field

from app.utils.custom_types import OrderStatus, created_at, closed_at


class CreateOrderItemRequest(BaseModel):
    product_id: UUID 
    quantity: int = Field(ge=0, default=1)
    price: int = Field(ge=0)


class CreateOrderRequest(BaseModel):
    full_name: str = Field(max_length=50)
    phone: str = Field(max_length=50)
    location: str = Field(max_length=255)
    telegram_id: Optional[int] = Field(default=None)

    delivery_date: datetime.date
    slot_from: datetime.time
    slot_to: datetime.time
    
    items: List[CreateOrderItemRequest]


class OrderItemResponce(BaseModel):
    product_id: UUID

    product_name: Optional[str] = None
    quantity: int
    price: int

    subtotal: Optional[int] = None

    class Config:
        from_attributes = True


class OrderResponce(BaseModel):
    id: UUID
    user_id: UUID

    full_name: str
    phone: str
    location: str

    status: OrderStatus
    total_sum: int

    created_at: datetime.datetime
    closed_at: Optional[datetime.datetime] = Field(default=None)

    delivery_date: datetime.date
    slot_from: datetime.time
    slot_to: datetime.time

    items: List[OrderItemResponce]

    class Config:
        from_attributes = True