from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class Location(Base):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(Text)
    phone = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def create(cls, session, name, address=None, phone=None, email=None):
        location = cls(name=name, address=address, phone=phone, email=email)
        session.add(location)
        session.commit()
        return location
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        location = cls.find_by_id(session, id)
        if not location:
            return None
        for key, value in kwargs.items():
            if hasattr(location, key):
                setattr(location, key, value)
        session.commit()
        return location
    
    @classmethod
    def delete(cls, session, id):
        location = cls.find_by_id(session, id)
        if not location:
            return False
        session.delete(location)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Location id={self.id} name={self.name} address={self.address} phone={self.phone} email={self.email}>"
