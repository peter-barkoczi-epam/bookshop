import controllers.user_controller as user_controller

from schemas.user_schema import UserSchema
from tests.factories import UserFactory
from unittest.mock import MagicMock


def test_get_all_users_unit(monkeypatch):
    users = [
        UserFactory.build(id=1, role_id=3),
        UserFactory.build(id=2, role_id=1)
    ]
    user_list_schema = UserSchema(many=True)
    mock_users = user_list_schema.dump(users)

    mock_service = MagicMock()
    mock_service.get_all.return_value = mock_users

    monkeypatch.setattr(user_controller, 'UserService', mock_service)

    result = user_controller.UserController.get_all.__wrapped__()

    assert result == mock_users
    mock_service.get_all.assert_called_once()

def test_get_user_by_id_unit(monkeypatch):
    user = UserFactory.build(id=1, role_id=3)
    
    user_schema = UserSchema()
    mock_user = user_schema.dump(user)

    mock_service = MagicMock()
    mock_service.get.return_value = mock_user

    monkeypatch.setattr(user_controller, 'UserService', mock_service)

    result = user_controller.UserController.get(1)

    assert result == mock_user
    mock_service.get.assert_called_once_with(1)

def test_create_user_unit(monkeypatch):
    user = UserFactory.build(id=1, role_id=2)

    user_schema = UserSchema()
    mock_user = user_schema.dump(user)

    mock_service = MagicMock()
    mock_service.create.return_value = (mock_user, 201)

    monkeypatch.setattr(user_controller, 'UserService', mock_service)

    result = user_controller.UserController.create()
    assert result == (mock_user, 201)
    mock_service.create.assert_called_once_with()

def test_delete_user_unit(monkeypatch):
    mock_service = MagicMock()
    mock_service.delete.return_value = ('User deleted successfully', 201)

    monkeypatch.setattr(user_controller, 'UserService', mock_service)

    result = user_controller.UserController.delete(1)
    assert result == ('User deleted successfully', 201)
    mock_service.delete.assert_called_once_with(1)

def test_update_user_unit(monkeypatch):
    user = UserFactory.build(id=1, role_id=2)

    user_schema = UserSchema()
    mock_user = user_schema.dump(user)

    mock_service = MagicMock()
    mock_service.update.return_value = (mock_user, 200)

    monkeypatch.setattr(user_controller, 'UserService', mock_service)

    result = user_controller.UserController.update(1)
    assert result == (mock_user, 200)
    mock_service.update.assert_called_once_with(1)