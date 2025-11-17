from unittest.mock import MagicMock
from types import SimpleNamespace

from data_access_objects.book_store_dao import BookStoreDao
from models.book_store_model import BookStore
from tests.factories import BookStoreItemFactory
from app import app as flask_app


def test_fetch_by_id_returns_book_store_item(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    mock_query = MagicMock()
    mock_query.get_or_404.return_value = book_store_item

    with flask_app.app_context():
        monkeypatch.setattr(BookStore, 'query', mock_query, raising=False)

    result = BookStoreDao.fetch_by_id(1)

    assert result == book_store_item
    mock_query.get_or_404.assert_called_once_with(1, description=BookStoreDao.STORE_ITEM_NOT_FOUND.format(1))


def test_fetch_all_returns_list(monkeypatch):
    book_store_items = [BookStoreItemFactory.build(id=1), BookStoreItemFactory.build(id=2)]
    mock_query = MagicMock()
    mock_query.all.return_value = book_store_items
    with flask_app.app_context():
        monkeypatch.setattr(BookStore, 'query', mock_query, raising=False)

    result = BookStoreDao.fetch_all()

    assert result == book_store_items
    mock_query.all.assert_called_once()


def test_create_calls_session_add_and_commit(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.book_store_dao.db', db_mock)

    BookStoreDao.create(book_store_item)

    session.add.assert_called_once_with(book_store_item)
    session.commit.assert_called_once()


def test_delete_fetches_and_deletes_item(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    mock_filter = MagicMock()
    mock_filter.first.return_value = book_store_item

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_filter
    with flask_app.app_context():
        monkeypatch.setattr(BookStore, 'query', mock_query, raising=False)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.book_store_dao.db', db_mock)

    BookStoreDao.delete(1)

    mock_query.filter_by.assert_called_once_with(id=1)
    session.delete.assert_called_once_with(book_store_item)
    session.commit.assert_called_once()


def test_update_calls_merge_and_commit(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.book_store_dao.db', db_mock)

    BookStoreDao.update(book_store_item)

    session.merge.assert_called_once_with(book_store_item)
    session.commit.assert_called_once()