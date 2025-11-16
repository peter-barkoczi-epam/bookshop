from database import db
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Booking(db.Model):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    delivery_address = Column(String(256), nullable=False)
    delivery_date = Column(Date, nullable=False)
    delivery_date = Column(DateTime, nullable=False)
    status_id = Column(Integer, ForeignKey("booking_status.id"), nullable=False)
    quantity = Column(Integer)
    user = relationship("User", back_populates="bookings")
    product = relationship("Product", back_populates="bookings")
    booking_status = relationship("BookingStatus", back_populates="bookings")

    def __repr__(self):
        return f"<Booking {self.id}>"
    