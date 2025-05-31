from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, date

from lib.models.base import Base

# Import ServiceClass here to avoid circular import issues
from lib.models.service_class import ServiceClass

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    service_class_id = Column(Integer, ForeignKey('service_classes.id'), nullable=True)
    weight = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, default='placed')
    pickup_date = Column(Date, nullable=False)
    pickup_time = Column(String, nullable=False)  # 'morning', 'afternoon', 'evening'
    special_instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    customer = relationship("Customer", back_populates="orders")
    service = relationship("Service", back_populates="orders")
    service_class = relationship("ServiceClass", back_populates="orders")
    status_history = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")
    comments = relationship("OrderComment", back_populates="order", cascade="all, delete-orphan")
    
    # Remove property for weight to use direct column access
    # @property
    # def weight(self):
    #     return self._weight
        
    # @weight.setter
    # def weight(self, value):
    #     if not isinstance(value, (int, float)) or value <= 0:
    #         raise ValueError("Weight must be a positive number")
    #     self._weight = value
    
    # Remove property for pickup_date to use direct column access
    # @property
    # def pickup_date(self):
    #     return self._pickup_date
        
    # @pickup_date.setter
    # def pickup_date(self, value):
    #     if isinstance(value, str):
    #         value = datetime.strptime(value, '%Y-%m-%d').date()
    #     if value < date.today():
    #         raise ValueError("Pickup date cannot be in the past")
    #     self._pickup_date = value
    
    @classmethod
    def create(cls, session, customer_id, service_id, weight, total_price, pickup_date, pickup_time, special_instructions):
        print(f"Creating order for customer_id={customer_id}, service_id={service_id}, weight={weight}, total_price={total_price}")
        order = cls(
            customer_id=customer_id,
            service_id=service_id,
            weight=weight,
            total_price=total_price,
            pickup_date=pickup_date,
            pickup_time=pickup_time,
            special_instructions=special_instructions,
            status="picked"  # or your default status
        )
        session.add(order)
        try:
            session.commit()
            print(f"Order committed successfully with id={order.id}")
        except Exception as e:
            print(f"Error committing order: {e}")
            session.rollback()
            raise
        return order
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def update(cls, session, id, **kwargs):
        from lib.models.order_status_history import OrderStatusHistory
        
        order = cls.find_by_id(session, id)
        if not order:
            return None
        
        if 'status' in kwargs and kwargs['status'] != order.status:
            history_entry = OrderStatusHistory(
                order_id=order.id,
                status=kwargs['status'],
                timestamp=datetime.utcnow()
            )
            session.add(history_entry)
        
        for key, value in kwargs.items():
            if hasattr(order, key):
                setattr(order, key, value)
        
        session.commit()
        return order
    
    @classmethod
    def delete(cls, session, id):
        order = cls.find_by_id(session, id)
        if not order:
            return False
        session.delete(order)
        session.commit()
        return True
    
    def __repr__(self):
        return f"<Order id={self.id} customer_id={self.customer_id} status={self.status}>"

    @classmethod
    def find_by_customer(cls, session, customer_id):
        return session.query(cls).filter_by(customer_id=customer_id).all()
