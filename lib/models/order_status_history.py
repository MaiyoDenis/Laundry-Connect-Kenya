from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class OrderStatusHistory(Base):
    __tablename__ = 'order_status_history'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    status = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="status_history")
    
    @classmethod
    def create(cls, session, order_id, status):
        history = cls(order_id=order_id, status=status)
        session.add(history)
        session.commit()
        return history
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        history = cls.find_by_id(session, id)
        if not history:
            return False
        session.delete(history)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<OrderStatusHistory id={self.id} order_id={self.order_id} status={self.status} timestamp={self.timestamp}>"
