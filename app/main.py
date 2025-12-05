from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import models, database

app = FastAPI(title = "Restaurant orders API")

def start():
    database.init_db()

@app.post("/menu/")
def createProduct(product: ProductCreate, db: Session = Depends(database.get_database)):
    new_product = models.Products(name = product.name, price = product.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/menu/")
def listProducts(db: Session = Depends(database.get_database)):
    products = db.query(models.Products).all()
    return products