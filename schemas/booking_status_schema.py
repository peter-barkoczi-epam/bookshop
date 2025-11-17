from database import db
from dependencies import ma
from models.role_model import Role

class BookingStatusSchema(ma.SQLAlchemySchema):

    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    name = ma.auto_field()