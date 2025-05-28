from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from lib.models.base import Base

DATABASE_URL = "sqlite:///laundryconnect.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
