from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from data_access_objects.booking_dao import BookingDao
from schemas.booking_schema import BookingSchema

bookingSchema = BookingSchema()
bookingListSchema = BookingSchema(many=True)

class BookingService:
    
    @staticmethod
    def get(booking_id: int):
        booking_data = BookingDao.fetch_by_id(booking_id)
        return bookingSchema.dump(booking_data)
    
    @staticmethod
    def get_all():
        return bookingListSchema.dump(BookingDao.fetch_all())
    
    @staticmethod
    def create():
        booking_req_json = request.get_json()
        try:
            booking_data = bookingSchema.load(booking_req_json)
            BookingDao.create(booking_data)
            return bookingSchema.dump(booking_data), 201
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")

    
    @staticmethod
    def delete(booking_id: int):
        BookingDao.fetch_by_id(booking_id)
        BookingDao.delete(booking_id)
        return {'message': 'Booking deleted successfully'}, 201
    
    @staticmethod
    def update(booking_id: int):
        try:
            booking_data = bookingSchema.dump(BookingDao.fetch_by_id(booking_id))
            booking_data.update(request.get_json())
            booking_data = bookingSchema.load(booking_data)
            BookingDao.update(booking_data)
            return bookingSchema.dump(booking_data), 204
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")
