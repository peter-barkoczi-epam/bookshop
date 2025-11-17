from unittest.mock import MagicMock
from types import SimpleNamespace

from data_access_objects.user_dao import UserDao
from models.user_model import User
from tests.factories import UserFactory
from app import app as flask_app


def test_fetch_by_id_returns_user(monkeypatch):
    user = UserFactory.build(id=1, role_id=2)

    mock_query = MagicMock()
    mock_query.get_or_404.return_value = user

    with flask_app.app_context():
        monkeypatch.setattr(User, 'query', mock_query, raising=False)

    result = UserDao.fetch_by_id(1)

    assert result == user
    mock_query.get_or_404.assert_called_once_with(1, description=UserDao.USER_NOT_FOUND.format(1))


def test_fetch_all_returns_list(monkeypatch):
    users = [UserFactory.build(id=1), UserFactory.build(id=2)]
    mock_query = MagicMock()
    mock_query.all.return_value = users
    with flask_app.app_context():
        monkeypatch.setattr(User, 'query', mock_query, raising=False)

    result = UserDao.fetch_all()

    assert result == users
    mock_query.all.assert_called_once()


def test_create_calls_session_add_and_commit(monkeypatch):
    user = UserFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.user_dao.db', db_mock)

    UserDao.create(user)

    session.add.assert_called_once_with(user)
    session.commit.assert_called_once()


def test_delete_fetches_and_deletes_item(monkeypatch):
    user = UserFactory.build(id=1)

    mock_filter = MagicMock()
    mock_filter.first.return_value = user

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_filter
    with flask_app.app_context():
        monkeypatch.setattr(User, 'query', mock_query, raising=False)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.user_dao.db', db_mock)

    UserDao.delete(1)

    mock_query.filter_by.assert_called_once_with(id=1)
    session.delete.assert_called_once_with(user)
    session.commit.assert_called_once()


def test_update_calls_merge_and_commit(monkeypatch):
    user = UserFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.user_dao.db', db_mock)

    UserDao.update(user)

    session.merge.assert_called_once_with(user)
    session.commit.assert_called_once()