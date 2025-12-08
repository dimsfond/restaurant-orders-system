import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from my_app.models import Base, MenuItem, Order, OrderItem
from my_app.utilities import compute_order_total

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind = engine, autoflush = False, autocommit = False)
Base.metadata.create_all(bind = engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_compute_order_total(db):
    menu_item1 = MenuItem(name="Burger", price=8.0)
    menu_item2 = MenuItem(name="Fries", price=4.0)
    db.add_all(menu_item1, menu_item2)
    db.commit()

    order = Order(total = 0.0)
    db.add(order)
    db.commit()

    order_item1 = OrderItem(order_id=order.id, menu_item_id=menu_item1.id, quantity=2)
    order_item2 = OrderItem(order_id=order.id, menu_item_id=menu_item2.id, quantity=3)
    db.add_all([order_item1, order_item2])
    db.commit()

    total = compute_order_total(order, db)
    assert total == 8.0 * 2 + 4.0 * 3