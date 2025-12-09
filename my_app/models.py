from sqlalchemy import Column, String, Integer, Float,ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key = True, index = True)
    table_number = Column(Integer, nullable = False)
    is_present = Column(Boolean, nullable = False)
    orders = relationship("Order", back_populates = "customer", cascade = "all, delete-orphan")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key = True, index = True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(String, default = "pending", nullable = False)
    total = Column(Float, nullable = False)
    customer = relationship("Customer", back_populates = "orders")
    items = relationship("OrderItem", back_populates = "order", cascade = "all, delete-orphan")

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable = False)
    order_items = relationship("OrderItem", back_populates = "menu_item")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key = True, index = True)
    quantity = Column(Integer, nullable = False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    order = relationship("Order", back_populates = "items")
    menu_item = relationship("MenuItem", back_populates = "order_items")

class OrderHistory(Base):
    __tablename__ = "order_history"
    id = Column(Integer, primary_key = True, index = True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable = False)
    previous_status = Column(String, nullable = False)
    new_status = Column(String, nullable = False)
    timestamp = Column(String, default=lambda: datetime.utcnow().isoformat())