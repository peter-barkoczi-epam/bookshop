from database import db
from dependencies import ma
from models.user_model import User
from models.role_model import RoleEnum
from marshmallow import fields

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

    role = fields.Method(
        serialize = "get_role",
        deserialize = "load_role"
    )

    def get_role(self, obj):
        try:
            return RoleEnum(obj.role_id).name
        except ValueError:
            return None
    
    def load_role(self, value):
        try:
            return RoleEnum[value].value
        except KeyError:
            return None