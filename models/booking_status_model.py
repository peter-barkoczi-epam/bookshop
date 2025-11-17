import enum

from database import db
from sqlalchemy import Column, Integer, String, event
from sqlalchemy.orm import relationship

class BookingStatusEnum(enum.Enum):
    SUBMITTED = 1
    REJECTED = 2
    APPROVED = 3
    CANCELLED = 4
    IN_DELIVERY = 5


class BookingStatus(db.Model):
    __tablename__ = "booking_status"
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False)
    bookings = relationship("Booking", back_populates="booking_status")

    def __repr__(self):
        return f"<Booking status {self.name}>"
    
@event.listens_for(BookingStatus.__table__, 'after_create')
def create_roles(*args, **kwargs):
    db.session.add(BookingStatus(id=BookingStatusEnum.SUBMITTED.value, name=str(BookingStatusEnum.SUBMITTED.name)))
    db.session.add(BookingStatus(id=BookingStatusEnum.REJECTED.value, name=str(BookingStatusEnum.REJECTED.name)))
    db.session.add(BookingStatus(id=BookingStatusEnum.APPROVED.value, name=str(BookingStatusEnum.APPROVED.name)))
    db.session.add(BookingStatus(id=BookingStatusEnum.CANCELLED.value, name=str(BookingStatusEnum.CANCELLED.name)))
    db.session.add(BookingStatus(id=BookingStatusEnum.IN_DELIVERY.value, name=str(BookingStatusEnum.IN_DELIVERY.name)))
    db.session.commit()