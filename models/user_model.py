import hashlib
import os

from database import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = relationship("Role", back_populates="users")
    bookings = relationship("Booking", back_populates="user")

    def __repr__(self) -> str:
        return f"<User {self.login}>"
    
    def hash_password(self, password: str):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        self.password_hash = salt + key
    
    def verify_password(self, password: str):
        salt, key = self.password_hash[:32], self.password_hash[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return key == new_key