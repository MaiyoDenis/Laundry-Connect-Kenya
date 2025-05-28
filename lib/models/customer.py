from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class Customer(Base):
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="customer", cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, session, name, phone, email=None, address=None):
        customer = cls(name=name, phone=phone, email=email, address=address)
        session.add(customer)
        session.commit()
        return customer
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        customer = cls.find_by_id(session, id)
        if not customer:
            return None
        for key, value in kwargs.items():
            if hasattr(customer, key):
                setattr(customer, key, value)
        session.commit()
        return customer
    
    @classmethod
    def delete(cls, session, id):
        customer = cls.find_by_id(session, id)
        if not customer:
            return False
        session.delete(customer)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Customer id={self.id} name={self.name} phone={self.phone}>"
