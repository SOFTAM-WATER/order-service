import datetime
from uuid import UUID
from typing import List
from pydantic import BaseModel, Field

class OrderItemDTO(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0)  
    price: int

class CreateOrderDTO(BaseModel):
    transaction_id: UUID
    user_id: UUID
    
    full_name: str = Field(min_length=1, max_length=256)
    phone: str = Field(min_length=5, max_length=20)
    location: str = Field(min_length=1, max_length=512)
    
    total_sum: int = Field(gt=0)
    
    delivery_date: datetime.date
    slot_from: datetime.time
    slot_to: datetime.time
    
    items: List[OrderItemDTO]