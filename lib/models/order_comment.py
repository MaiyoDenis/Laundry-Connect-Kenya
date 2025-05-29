from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from lib.models.base import Base

class OrderComment(Base):
    __tablename__ = 'order_comments'
    
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    order = relationship("Order", back_populates="comments")
    customer = relationship("Customer", back_populates="comments")
    
    @classmethod
    def create(cls, session, order_id, customer_id, comment):
        order_comment = cls(order_id=order_id, customer_id=customer_id, comment=comment)
        session.add(order_comment)
        session.commit()
        return order_comment
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        comment = cls.find_by_id(session, id)
        if not comment:
            return False
        session.delete(comment)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<OrderComment id={self.id} order_id={self.order_id} customer_id={self.customer_id} comment={self.comment[:20]}...>"
