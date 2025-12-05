from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, session
from .models import Base

DATABASE_URL = "sqlite:///./restaurant.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
session = sessionmaker(bind = engine, autocommit = False, autoflush = False)

def init_db():
    Base.metadata.create_all(bind = engine)
    
def get_db():
    dbSession = session()
    try:
        yield dbSession
    finally:
        dbSession.close()