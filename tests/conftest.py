# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from my_app.models import Base, Customer, MenuItem
from my_app.main import app
from my_app.database import get_db

# In-memory SQLite DB
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create all tables once
Base.metadata.create_all(bind=engine)

# DB session fixture
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

# FastAPI client fixture
@pytest.fixture
def client(db_session):
    # Seed some initial data
    customer1 = Customer(table_number=1, is_present=True)
    menu_item1 = MenuItem(name="Margherita Pizza", price=8.50)
    menu_item2 = MenuItem(name="Espresso", price=2.50)
    db_session.add_all([customer1, menu_item1, menu_item2])
    db_session.commit()

    # Override dependency
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.pop(get_db, None)
