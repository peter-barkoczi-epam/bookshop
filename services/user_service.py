from flask import request, jsonify
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from data_access_objects.user_dao import UserDao
from schemas.user_schema import UserSchema

userSchema = UserSchema()
userListSchema = UserSchema(many=True)

class UserService:
    
    @staticmethod
    def get(user_id: int):
        user_data = UserDao.fetch_by_id(user_id)
        return userSchema.dump(user_data)
    
    @staticmethod
    def get_all():
        return userListSchema.dump(UserDao.fetch_all())
    
    @staticmethod
    def create():
        user_req_json = request.get_json()
        password = user_req_json.pop('password', None)
        if not password:
            return jsonify(detail='Impossible to create a new user. Filed "password" is not set.', status=400, title="Bad Request", type="about:blank")
        user_data = userSchema.load(user_req_json)
        user_data.hash_password(password)
        UserDao.create(user_data)
        return userSchema.dump(user_data), 201
    
    @staticmethod
    def delete(user_id: int):
        UserDao.fetch_by_id(user_id)
        UserDao.delete(user_id)
        return {'message': 'User deleted successfully'}, 201
    
    @staticmethod
    def update(user_id: int):
        try:
            user_data = userSchema.dump(UserDao.fetch_by_id(user_id))
            user_data.update(request.json())
            user_data = userSchema.load(user_data)
            UserDao.update(user_data)
            return userSchema.dump(user_data), 404
        except ValidationError as error:
            return jsonify(detail=str(error), status=400, title="Bad Request", type="about:blank")
        except IntegrityError as error:
            return jsonify(detail=error.args[0], status=400, title="Bad Request", type="about:blank")
