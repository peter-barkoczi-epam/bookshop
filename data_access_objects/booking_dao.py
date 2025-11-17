from database import db
from models.bookings_model import Booking
from typing import List

class BookingDao:

    BOOKING_NOT_FOUND = "Booking not found for id: {}"

    @staticmethod
    def create(booking: Booking):
        db.session.add(booking)
        db.session.commit()

    @staticmethod
    def fetch_by_id(booking_id: int) -> Booking:
        return Booking.query.get_or_404(
            booking_id,
            description=BookingDao.BOOKING_NOT_FOUND.format(booking_id)
        )
    
    @staticmethod
    def fetch_all() -> List[Booking]:
        return Booking.query.all()
    
    @staticmethod
    def delete(booking_id: int) -> None:
        item = Booking.query.filter_by(id=booking_id).first()
        db.session.delete(item)
        db.session.commit()
    
    @staticmethod
    def update(booking_data):
        db.session.merge(booking_data)
        db.session.commit()
