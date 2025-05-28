from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class Service(Base):
    __tablename__ = 'services'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price_per_unit = Column(Float, nullable=False)
    unit = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    orders = relationship("Order", back_populates="service", cascade="all, delete-orphan")
    
    @classmethod
    def create(cls, session, name, price_per_unit, description=None, unit=None):
        service = cls(name=name, price_per_unit=price_per_unit, description=description, unit=unit)
        session.add(service)
        session.commit()
        return service
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        service = cls.find_by_id(session, id)
        if not service:
            return None
        for key, value in kwargs.items():
            if hasattr(service, key):
                setattr(service, key, value)
        session.commit()
        return service
    
    @classmethod
    def delete(cls, session, id):
        service = cls.find_by_id(session, id)
        if not service:
            return False
        session.delete(service)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Service id={self.id} name={self.name} price_per_unit={self.price_per_unit} description={self.description} unit={self.unit}>"
