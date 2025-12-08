from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Customer, MenuItem
from app.main import app
from app.database import get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)
Base.metadata.create_all(bind = engine)

@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db_session):
    customer1 = Customer(table_number = 1, is_present = True)
    menu_item1 = MenuItem(name="Margherita Pizza", price=8.50)
    menu_item2 = MenuItem(name="Espresso", price=2.50)
    db_session.add_all([customer1, menu_item1, menu_item2])
    db_session.commit()

    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides = override_get_db

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.pop(get_db, None)

def test_create_order_success(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 2},
            {"menu_item_id": 2, "quantity": 1} 
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["customer_id"] == 1
    assert data["status"] == "pending"
    assert abs(data["total"] - 19.5) < 1e-6
    assert isinstance(data["items"], list) and len(data["items"]) == 2

def test_create_order_invalid_quantity(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 0},
            {"menu_item_id": 2, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 400, response.text
    data = response.json()
    assert "Invalid quantity" in data["detail"]

def test_create_order_non_existent_menu_item(client):
    payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 999, "quantity": 1},
            {"menu_item_id": 2, "quantity": 1}
        ]
    }
    response = client.post("/orders/", json = payload)
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Menu Item not found"

def test_patch_order_status_sucess(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 1}
        ]
    }
    order_response = client.post("/orders/", json = creating_order_payload)
    order_id = order_response.json()["id"]

    payload = {"status": "preparing"}
    response = client.patch(f"/orders/{order_id}/status", json = payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "preparing"

def test_patch_order_status_invalid(client):
    creating_order_payload = {
        "customer_id": 1,
        "items": [
            {"menu_item_id": 1, "quantity": 1}
        ]
    }
    order_response = client.post("/orders/", json = creating_order_payload)
    order_id = order_response.json()["id"]

    payload = {"status": "cooking"}
    response = client.patch(f"/orders/{order_id}/status", json = payload)
    assert response.status_code == 400, response.text
    data = response.json()
    assert "Invalid Status" in data["detail"]
