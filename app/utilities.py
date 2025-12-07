from fastapi import HTTPException
from models import Order, OrderItem, MenuItem
from app import database
from sqlalchemy.orm import Session
from fastapi import Depends

def compute_order_total(order: Order, db: Session) -> float:
    total = 0.0
    for item in order.items:
        if item.menu_item is None:
            item.menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if item.menu_item is None:
            raise HTTPException(status_code=404, detail=f"Menu item {item.menu_item_id} not found")
        total += item.quantity * item.menu_item.price
    return round(total, 2)