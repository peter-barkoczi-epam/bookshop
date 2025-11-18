from authenticator import auth
from services.user_service import UserService

class UserController:

    @staticmethod
    @auth.login_required(role='customer')
    def get(user_id: int):
        return UserService.get(user_id)

    @staticmethod
    @auth.login_required(role='admin')
    def get_all():
        return UserService.get_all()
    
    @staticmethod
    def create():
        return UserService.create()
    
    @staticmethod
    def delete(user_id: int):
        return UserService.delete(user_id)
    
    @staticmethod
    def update(user_id: int):
        return UserService.update(user_id)
