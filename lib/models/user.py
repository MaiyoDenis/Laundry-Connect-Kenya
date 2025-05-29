from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from lib.models.base import Base
from passlib.hash import bcrypt

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_customer = Column(Boolean, default=True)
    is_manager = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = bcrypt.hash(password)
    
    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
    @classmethod
    def create(cls, session, username, password, is_customer=True, is_manager=False):
        user = cls(username=username, is_customer=is_customer, is_manager=is_manager)
        user.set_password(password)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def find_by_username(cls, session, username):
        return session.query(cls).filter_by(username=username).first()
    
    def __repr__(self):
        return f"<User id={self.id} username={self.username} customer={self.is_customer} manager={self.is_manager}>"
