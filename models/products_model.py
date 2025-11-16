from database import db
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Product(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(256), nullable=False)
    author = Column(String(256), nullable=False)
    price = Column(Float, nullable=False)
    image_path = Column(String(256), nullable=False)
    bookings = relationship("Booking", back_populates="product")
    book_stores = relationship("BookStore", back_populates="product")

    def __repr__(self):
        return f"<Booking {self.id}>"
    