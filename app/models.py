from sqlalchemy import Column, String, Integer, Float,ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable = False)
    orders = relationship("Order", back_populates = "customer", cascade = "all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default = "pending", nullable = False)
    customer = relationship("Customer", back_populates = "orders")
    total = Column(Float, nullable = False)

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable = False)

class OrderItem(base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key = True, index = True)
    quantity = Column(Integer, nullable = False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    order = relationship("Order", back_populates = "items")