from database import db
from dependencies import ma
from models.bookings_model import Booking
from models.booking_status_model import BookingStatusEnum
from schemas.user_schema import UserSchema
from schemas.product_schema import ProductSchema
from marshmallow import fields

class BookingSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Booking
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    user_id = ma.auto_field()
    product_id = ma.auto_field()
    delivery_address = ma.auto_field()
    delivery_date = ma.auto_field()
    delivery_time = ma.auto_field()
    status_id = ma.auto_field()
    quantity = ma.auto_field()

    user = fields.Nested(UserSchema, dump_only=True)
    product = fields.Nested(ProductSchema, dump_only=True)
    status = fields.Method(
        serialize = "get_status",
        deserialize = "load_status"
    )

    def get_status(self, obj):
        try:
            return BookingStatusEnum(obj.status_id).name
        except ValueError:
            return None
    
    def load_status(self, value):
        try:
            return BookingStatusEnum[value].value
        except KeyError:
            return None

