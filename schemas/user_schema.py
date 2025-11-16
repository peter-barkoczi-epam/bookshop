from database import db
from dependencies import ma
from models.user_model import User

class UserSchema(ma.SQLAlchemySchema):

    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
    
    id = ma.auto_field()
    name = ma.auto_field()
    role_id = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    address = ma.auto_field()
    login = ma.auto_field()
    password = ma.auto_field()