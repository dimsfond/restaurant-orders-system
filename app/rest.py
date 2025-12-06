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