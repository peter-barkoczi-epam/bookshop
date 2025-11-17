from unittest.mock import MagicMock
from types import SimpleNamespace

from data_access_objects.booking_dao import BookingDao
from models.bookings_model import Booking
from tests.factories import BookingFactory
from app import app as flask_app


def test_fetch_by_id_returns_booking(monkeypatch):
    booking = BookingFactory.build(id=1)

    mock_query = MagicMock()
    mock_query.get_or_404.return_value = booking

    with flask_app.app_context():
        monkeypatch.setattr(Booking, 'query', mock_query, raising=False)

    result = BookingDao.fetch_by_id(1)

    assert result == booking
    mock_query.get_or_404.assert_called_once_with(1, description=BookingDao.BOOKING_NOT_FOUND.format(1))


def test_fetch_all_returns_list(monkeypatch):
    bookings = [BookingFactory.build(id=1), BookingFactory.build(id=2)]
    mock_query = MagicMock()
    mock_query.all.return_value = bookings
    with flask_app.app_context():
        monkeypatch.setattr(Booking, 'query', mock_query, raising=False)

    result = BookingDao.fetch_all()

    assert result == bookings
    mock_query.all.assert_called_once()


def test_create_calls_session_add_and_commit(monkeypatch):
    booking = BookingFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.booking_dao.db', db_mock)

    BookingDao.create(booking)

    session.add.assert_called_once_with(booking)
    session.commit.assert_called_once()


def test_delete_fetches_and_deletes_item(monkeypatch):
    booking = BookingFactory.build(id=1)

    mock_filter = MagicMock()
    mock_filter.first.return_value = booking

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_filter
    with flask_app.app_context():
        monkeypatch.setattr(Booking, 'query', mock_query, raising=False)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.booking_dao.db', db_mock)

    BookingDao.delete(1)

    mock_query.filter_by.assert_called_once_with(id=1)
    session.delete.assert_called_once_with(booking)
    session.commit.assert_called_once()


def test_update_calls_merge_and_commit(monkeypatch):
    booking = BookingFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.booking_dao.db', db_mock)

    BookingDao.update(booking)

    session.merge.assert_called_once_with(booking)
    session.commit.assert_called_once()