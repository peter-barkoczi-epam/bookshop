from database import db
from dependencies import ma
from models.bookings_model import Booking

class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Booking
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    user_id = ma.auto_field()
    product_id = ma.auto_field()
    delivery_address = ma.auto_field()
    delivery_date = ma.auto_field()
    delivery_date = ma.auto_field()
    status_id = ma.auto_field()
    quantity = ma.auto_field()