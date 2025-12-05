from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from models import Customer, Order, OrderItem, MenuItem

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