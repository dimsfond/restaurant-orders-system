from fastapi import FastAPI, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app import database
from models import Customer, Order, OrderItem, MenuItem
import schemas, utilities
from typing import List, Optional

app = FastAPI(title = "Restaurant orders API")

def start_db():
    database.init_db()

@app.post("/customers/", response_model = dict)
def add_customer(table_number: int, db: Session = Depends(database.get_db)):
    customer = Customer(table_number)
    db.add(customer)
    db.commit()
    db.refresh(customer)

    return {id: customer.id, table_number: customer.table_number}

@app.delete("/customers/{id}", response_model = dict)
def delete_customer(id: int, db: Session = Depends(database.get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    db.delete(customer)
    db.commit()

    return {"detail: Customer {id} left the restaurant without eating and he, along with his unprepared orders, were deleted"}

@app.get("/customers/active", response_model = list[dict])
def list_present_customers(db: Session = Depends(database.get_db)):
    customers = db.query(Customer).filter(Customer.is_present == True).all()

    return [
        {
            "id": customer.id,
            "table_number": customer.table_number,
        }
        for customer in customers
    ]

@app.patch("customers/{id}/leave", response_model = dict)
def customer_leaves(id: int, db: Session = Depends(database.get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer_not found")
    customer.is_present = False
    db.commit()
    db.refresh(customer)

    return {"detail": "Customer {id} has paid and left"}

@app.get("/menu/", response_model=list[dict])
def get_menu(db: Session = Depends(database.get_db)):
    menu = db.query(MenuItem).all()

    return [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price
        }
        for item in menu
    ]

@app.post("/menu/", response_model = dict)
def add_menu_item(name: str, price: float, db: Session = Depends(database.get_db)):
    item = MenuItem(name, price)
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "name": item.name,
        "price": item.price
    }

@app.patch("menu/{id}", response_model = dict)
def update_item(id: int, name: str | None, price: float | None, db: Session = Depends(database.get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = "Item not found")
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "name": item.name,
        "price": item.price
    }

@app.delete("menu/{id}", response_model = dict)
def delete_item(id, db: Session = Depends(database.get_db)):
    item = db.query(MenuItem).filter(MenuItem.id == id).first()
    if not item:
        raise HTTPException(status_code = 404, detail = "Item not found")
    db.delete(item)
    db.commit()

    return {"detail": "Item {id} deleted from the menu"}

@app.post("/orders/", response_model = schemas.OrderResponse)
def create_order(payload: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    customer = db.query(Customer).filter(Customer.id == payload.customer_id).first()
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    order = Order(customer_id = payload.customer_id, status = "pending", total = 0.0)
    db.add(order)
    db.flush()
    for item in payload.items:
        menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
        if not menu_item:
            raise HTTPException(status = 404, detail = "Menu Item not found")
        order_item = OrderItem(quantity = item.quantity, order_id = order.id, menu_item_id = menu_item.id)
        db.add(order_item)
    db.commit()
    db.refresh(order)
    order.total = utilities.compute_order_total(order, db)
    db.commit()
    db.refresh(order)

    return order

@app.patch("/orders/{id}/status", response_model = schemas.OrderResponse)
def update_order_status(id: int, status_update: schemas.StatusUpdate, db: Session = Depends(database.get_db)):
    try:
        updated_status = schemas.OrderStatus(status_update.status)
    except:
        raise HTTPException(status_code = 400, detail = f"Invalid status. Allowed values are {[s.value for s in schemas.OrderStatus]}")
    order = db.query(Order).filter(Order.id == id).first()
    if not order:
        raise HTTPException(status_code = 404, detail = "Order not found")
    order.status = updated_status.value
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