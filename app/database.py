from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from .models import Base

DATABASE_URL = "sqlite:///./restaurant.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind = engine, autocommit = False, autoflush = False)

Base.metadata.create_all(bind = engine)
def get_database():
    session_db = session()
    try:
        yield session_db
    finally:
        session_db.close()