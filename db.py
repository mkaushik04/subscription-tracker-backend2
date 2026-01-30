from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./subscriptions.db"

#Database engine created 
engine = create_engine(
    DATABASE_URL,
    
    connect_args={"check_same_thread": False}
)

#Session factory
SessionLocal = sessionmaker(
    autocommit = False, #My decision when data should be saved 
    autoflush = False, #Changes sent only when I explicitely tell to do so
    bind = engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        