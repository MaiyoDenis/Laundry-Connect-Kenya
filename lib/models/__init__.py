# lib/models/__init__.py

from lib.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .customer import Customer
from .service import Service
from .order import Order
from .location import Location
from .order_status_history import OrderStatusHistory
from .service_class import ServiceClass
from .user import User

DATABASE_URL = "sqlite:///laundryconnect.db"

engine = create_engine(DATABASE_URL, echo=False)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

__all__ = [
    "Base",
    "engine",
    "Session",
    "Customer",
    "Service",
    "Order",
    "Location",
    "OrderStatusHistory",
    "create_tables",
    "ServiceClass",
    "User",
]

# Create all tables
def create_tables():
    Base.metadata.create_all(engine, checkfirst=True)
