from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class ServiceClass(Base):
    __tablename__ = 'service_classes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    price_multiplier = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="service_class")
    
    @classmethod
    def create(cls, session, name, price_multiplier=1.0, description=None):
        service_class = cls(name=name, price_multiplier=price_multiplier, description=description)
        session.add(service_class)
        session.commit()
        return service_class
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        service_class = cls.find_by_id(session, id)
        if not service_class:
            return None
        for key, value in kwargs.items():
            if hasattr(service_class, key):
                setattr(service_class, key, value)
        session.commit()
        return service_class
    
    @classmethod
    def delete(cls, session, id):
        service_class = cls.find_by_id(session, id)
        if not service_class:
            return False
        session.delete(service_class)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<ServiceClass id={self.id} name={self.name} multiplier={self.price_multiplier}>"
