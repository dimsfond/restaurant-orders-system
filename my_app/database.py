import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from .models import Base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./restaurant.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)

def init_db():
    Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()