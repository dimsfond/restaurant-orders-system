from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class MenuItemCreate(BaseModel):
    name: str
    price: float

class MenuItemResponse(BaseModel):
    id: int
    name: str
    price: float
    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    quantity: int
    menu_item_id: int

class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    menu_item: Optional[MenuItemResponse] = None
    class Config:
        orm_mode = True

class OrderStatus(str, Enum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    served = "served"
    paid = "paid"

class OrderCreate(BaseModel):
    customer_id: int
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id: int
    customer_id: int
    status: OrderStatus
    total: float
    items: List[OrderItemResponse] = []
    class Config:
        orm_mode = True

class StatusUpdate(BaseModel):
    status: OrderStatus