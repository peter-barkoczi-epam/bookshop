from unittest.mock import MagicMock
import services.user_service as user_service
from data_access_objects.user_dao import UserDao
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from tests.factories import UserFactory

def test_user_service_create_success(monkeypatch):
    payload = UserFactory.create_payload()
    payload['password'] = 'secret'

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(user_service, 'request', dummy_request)

    user_obj = UserFactory.build(id=42)
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(load=lambda data: user_obj, dump=lambda u: {'id': u.id, 'login': u.login}))

    created = {}
    def capture_create(u):
        created['user'] = u
    monkeypatch.setattr(UserDao, 'create', capture_create)

    monkeypatch.setattr(user_obj, 'hash_password', MagicMock())

    result, status = user_service.UserService.create()

    assert status == 201
    assert result['login'] == user_obj.login
    assert 'user' in created
    user_obj.hash_password.assert_called_once()

def test_user_service_create_without_password(monkeypatch, app_ctx):
    payload = UserFactory.create_payload()

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(user_service, 'request', dummy_request)

    result = user_service.UserService.create()

    if hasattr(result, 'get_json'):
        assert result.get_json()['status'] == 400
    else:
        assert 'status' in result

def test_user_service_create_validation_error(monkeypatch, app_ctx):
    payload = UserFactory.create_payload()
    payload['password'] = 'secret'
    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(user_service, 'request', dummy_request)

    def raise_validation(data):
        raise ValidationError("bad data")
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(load=raise_validation))

    result = user_service.UserService.create()
    assert result.get_json()['status'] == 400

def test_user_service_create_integrity_error(monkeypatch, app_ctx):
    payload = UserFactory.create_payload()
    payload['password'] = 'secret'
    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(user_service, 'request', dummy_request)

    def raise_integrity(data):
        raise IntegrityError("duplicate", None, None)
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(load=raise_integrity))

    result = user_service.UserService.create()
    assert result.get_json()['status'] == 400

def test_user_service_get_all(monkeypatch):
    users = [UserFactory.build(id=1), UserFactory.build(id=2)]
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_all', lambda: users)
    monkeypatch.setattr(user_service, 'userListSchema', MagicMock(dump=lambda x: [{'id': user.id, 'login': user.login} for user in users]))

    result = user_service.UserService.get_all()
    assert isinstance(result, list)
    assert result == [{'id': 1, 'login': 'test1'}, {'id': 2, 'login': 'test2'}]

def test_user_service_get_by_id(monkeypatch):
    user = UserFactory.build(id=5)
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_by_id', lambda id: user)
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(dump=lambda x: {'id': x.id, 'login': x.login}))

    result = user_service.UserService.get(5)
    assert result['id'] == 5

def test_user_service_delete(monkeypatch, app_ctx):
    user = UserFactory.build(id=3)
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_by_id', lambda id: user)

    deleted = {}
    def capture_delete(user):
        deleted['user'] = user
    monkeypatch.setattr(UserDao, 'delete', capture_delete)

    result, status = user_service.UserService.delete(3)
    assert status == 201
    assert result['message'] == 'User deleted successfully'

def test_user_service_update_success(monkeypatch, app_ctx):
    user = UserFactory.build(id=1, address='old_address')
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_by_id', lambda id: user)
    monkeypatch.setattr(user_service, 'request', MagicMock(get_json=lambda: {'address': 'new_address'}))
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(
        dump=lambda x: {'id': x.id, 'address': x.address},
        load=lambda data: UserFactory.build(id=data['id'], address=data['address'])
    ))
    updated = {}
    def capture_update(user):
        updated['user'] = user
    monkeypatch.setattr(UserDao, 'update', capture_update)
    result, status = user_service.UserService.update(1)
    assert status == 200
    assert result['address'] == 'new_address'

def test_user_service_update_validation_error(monkeypatch, app_ctx):
    user = UserFactory.build(id=1, login='oldlogin')
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_by_id', lambda id: user)
    monkeypatch.setattr(user_service, 'request', MagicMock(get_json=lambda: {'login': 'newlogin'}))
    def raise_validation(data):
        raise ValidationError("bad data")
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(
        dump=lambda x: {'id': x.id, 'login': x.login},
        load=raise_validation
    ))
    result = user_service.UserService.update(1)
    assert result.get_json()['status'] == 400

def test_user_service_update_integrity_error(monkeypatch, app_ctx):
    user = UserFactory.build(id=1, login='oldlogin')
    monkeypatch.setattr('data_access_objects.user_dao.UserDao.fetch_by_id', lambda id: user)
    monkeypatch.setattr(user_service, 'request', MagicMock(get_json=lambda: {'login': 'oldlogin'}))
    def raise_integrity(data):
        raise IntegrityError("duplicate", None, None)
    monkeypatch.setattr(user_service, 'userSchema', MagicMock(
        dump=lambda x: {'id': x.id, 'login': x.login},
        load=raise_integrity
    ))
    result = user_service.UserService.update(1)
    assert result.get_json()['status'] == 400