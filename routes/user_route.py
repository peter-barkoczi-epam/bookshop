from flask import request

from controllers.user_controller import UserController


def user_control():
    if request.method == 'POST':
        return UserController.create()
    else:
        return UserController.get_all()

def user_manipulation(user_id: int):
    if request.method == 'GET':
        return UserController.get(user_id)
    elif request.method == 'PUT':
        return UserController.update(user_id)
    else:
        return UserController.delete(user_id)
