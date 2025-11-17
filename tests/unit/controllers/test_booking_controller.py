import controllers.booking_controller as booking_controller

from schemas.booking_schema import BookingSchema
from tests.factories import BookingFactory
from unittest.mock import MagicMock


def test_get_all_bookings_unit(monkeypatch):
    bookings = [
        BookingFactory.build(id=1),
        BookingFactory.build(id=2)
    ]
    booking_list_schema = BookingSchema(many=True)
    mock_bookings = booking_list_schema.dump(bookings)

    mock_service = MagicMock()
    mock_service.get_all.return_value = mock_bookings

    monkeypatch.setattr(booking_controller, 'BookingService', mock_service)

    # get_all is not decorated, call directly
    result = booking_controller.BookingController.get_all()

    assert result == mock_bookings
    mock_service.get_all.assert_called_once()

def test_get_booking_by_id_unit(monkeypatch):
    booking = BookingFactory.build(id=1)
    
    booking_schema = BookingSchema()
    mock_booking = booking_schema.dump(booking)

    mock_service = MagicMock()
    mock_service.get.return_value = mock_booking

    monkeypatch.setattr(booking_controller, 'BookingService', mock_service)

    result = booking_controller.BookingController.get(1)

    assert result == mock_booking
    mock_service.get.assert_called_once_with(1)

def test_create_booking_unit(monkeypatch):
    booking = BookingFactory.build(id=1)

    booking_schema = BookingSchema()
    mock_booking = booking_schema.dump(booking)

    mock_service = MagicMock()
    mock_service.create.return_value = (mock_booking, 201)

    monkeypatch.setattr(booking_controller, 'BookingService', mock_service)

    result = booking_controller.BookingController.create()
    assert result == (mock_booking, 201)
    mock_service.create.assert_called_once_with()

def test_delete_booking_unit(monkeypatch):
    mock_service = MagicMock()
    mock_service.delete.return_value = ('booking deleted successfully', 201)

    monkeypatch.setattr(booking_controller, 'BookingService', mock_service)

    result = booking_controller.BookingController.delete(1)
    assert result == ('booking deleted successfully', 201)
    mock_service.delete.assert_called_once_with(1)

def test_update_booking_unit(monkeypatch):
    booking = BookingFactory.build(id=1)

    booking_schema = BookingSchema()
    mock_booking = booking_schema.dump(booking)

    mock_service = MagicMock()
    mock_service.update.return_value = (mock_booking, 200)

    monkeypatch.setattr(booking_controller, 'BookingService', mock_service)

    result = booking_controller.BookingController.update(1)
    assert result == (mock_booking, 200)
    mock_service.update.assert_called_once_with(1)