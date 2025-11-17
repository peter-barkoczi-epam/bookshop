from authenticator import auth
from services.booking_service import BookingService

class BookingController:

    @staticmethod
    def get(booking_id: int):
        return BookingService.get(booking_id)

    @staticmethod
    # @auth.login_required
    def get_all():
        return BookingService.get_all()
    
    @staticmethod
    def create():
        return BookingService.create()
    
    @staticmethod
    def delete(booking_id: int):
        return BookingService.delete(booking_id)
    
    @staticmethod
    def update(booking_id: int):
        return BookingService.update(booking_id)
