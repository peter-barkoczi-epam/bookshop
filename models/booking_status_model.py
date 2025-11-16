from database import db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class BookingStatus(db.Model):
    __tablename__ = "booking_status"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    bookings = relationship("Booking", back_populates="booking_status")

    def __repr__(self):
        return f"<Booking status {self.name}>"