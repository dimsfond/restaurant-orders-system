from my_app import database, schemas, utilities
from my_app.models import Customer, Order, OrderItem, MenuItem
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

logging.basicConfig(level = logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title = "Restaurant orders API")

@app.on_event("startup")
def startup_event():
    database.init_db()

@app.post("/orders/", response_model = schemas.OrderResponse)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    for i, item in enumerate(payload.items):
        if item.quantity <= 0:
            raise HTTPException(status_code = 400, detail = f"Invalid quantity for item {i}: must be >= 1")
    order = Order(customer_id = payload.customer_id, status = "pending", total = 0.0)
    db.add(order)
    db.flush()
    try:
        for item in payload.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            if not menu_item:
                db.rollback()
                raise HTTPException(status_code = 404, detail = "Menu Item not found")
            if menu_item.price <= 0:
                db.rollback()
                raise HTTPException(status_code = 400, detail=f"Invalid price for menu item {menu_item.id}: must be greater than 0")
            order_item = OrderItem(quantity = item.quantity, order_id = order.id, menu_item_id = menu_item.id)
            db.add(order_item)
        db.commit()
        db.refresh(order)
        order.total = utilities.compute_order_total(order, db)
        db.commit()
        db.refresh(order)
        return order
    except HTTPException:
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code = 500, detail = "Internal Server Error")

@app.patch("/orders/{id}/status", response_model = schemas.OrderResponse)
def update_order_status(id: int, status_update: schemas.StatusUpdate, db: Session = Depends(database.get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    order.status = status_update.status.value
    db.commit()
    db.refresh(order)

    return order

@app.get("/orders/{id}", response_model = schemas.OrderResponse)
def list_order_details(id: int, db: Session = Depends(database.get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    for item in order.items:
        if item.menu_item is None:
            item.menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
    
    return order

@app.get("/orders/", response_model = list[schemas.OrderResponse])
def list_orders(status: Optional[schemas.OrderStatus] = None, db: Session = Depends(database.get_db)):
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status.value)
    orders = query.all()
    for order in orders:
        for item in order.items:
            if item.menu_item is None:
                item.menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
    
    return orders

@app.delete("/orders/{id}", response_model = dict)
def delete_order(id: int, db: Session = Depends(database.get_db)):
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    db.delete(order)
    db.commit()

    return {"detail": f"Order {id} has been deleted"}