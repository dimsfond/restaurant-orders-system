import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from my_app.models import Base, Customer, MenuItem, Order, OrderItem
from my_app.main import app
from my_app.database import get_db

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    #delete all tables before a new test
    session.query(OrderItem).delete()
    session.query(Order).delete()
    session.query(MenuItem).delete()
    session.query(Customer).delete()
    session.commit()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    customer1 = Customer(table_number=1, is_present=True)
    menu_item1 = MenuItem(name="Margherita Pizza", price=8.50)
    menu_item2 = MenuItem(name="Espresso", price=2.50)
    db_session.add_all([customer1, menu_item1, menu_item2])
    db_session.commit()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.pop(get_db, None)
