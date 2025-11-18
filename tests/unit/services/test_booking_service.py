from unittest.mock import MagicMock
import services.booking_service as booking_service
from data_access_objects.booking_dao import BookingDao
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from tests.factories import BookingFactory

def test_booking_service_create_success(monkeypatch):
    payload = BookingFactory.create_payload()

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(booking_service, 'request', dummy_request)

    booking_obj = BookingFactory.build(id=42)
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(load=lambda data: booking_obj, dump=lambda b: {'id': b.id, 'delivery_address': b.delivery_address}))

    created = {}
    def capture_create(b):
        created['booking'] = b
    monkeypatch.setattr(BookingDao, 'create', capture_create)

    result, status = booking_service.BookingService.create()

    assert status == 201
    assert result['delivery_address'] == booking_obj.delivery_address
    assert 'booking' in created

def test_booking_service_create_validation_error(monkeypatch, app_ctx):
    payload = BookingFactory.create_payload(quantity="5")
    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(booking_service, 'request', dummy_request)

    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(load=raise_validation))

    result = booking_service.BookingService.create()
    assert result.get_json()['status'] == 400

def test_booking_service_create_integrity_error(monkeypatch, app_ctx): 
    payload = BookingFactory.create_payload(product_id=1000)

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(booking_service, 'request', dummy_request)

    booking_obj = BookingFactory.build(id=42)
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(load=lambda data: booking_obj))

    def raise_integrity(b):
        raise IntegrityError("There is no product with this ID", params=None, orig=None)
    monkeypatch.setattr(BookingDao, 'create', raise_integrity)

    result = booking_service.BookingService.create()
    assert result.get_json()['status'] == 400

def test_booking_service_get_all(monkeypatch):
    bookings = [
        BookingFactory.build(id=1),
        BookingFactory.build(id=2)
    ]
    booking_list_schema = booking_service.bookingListSchema
    monkeypatch.setattr(BookingDao, 'fetch_all', MagicMock(return_value=bookings))
    monkeypatch.setattr(booking_service, 'bookingListSchema', booking_list_schema)

    result = booking_service.BookingService.get_all()

    expected = booking_list_schema.dump(bookings)
    assert result == expected

def test_booking_service_get(monkeypatch):
    booking = BookingFactory.build(id=1)

    booking_schema = booking_service.bookingSchema
    monkeypatch.setattr(BookingDao, 'fetch_by_id', MagicMock(return_value=booking))
    monkeypatch.setattr(booking_service, 'bookingSchema', booking_schema)

    result = booking_service.BookingService.get(1)

    expected = booking_schema.dump(booking)
    assert result == expected

def test_booking_service_delete(monkeypatch):
    mock_booking = BookingFactory.build(id=1)

    monkeypatch.setattr(BookingDao, 'fetch_by_id', MagicMock(return_value=mock_booking))
    deleted = {}
    def capture_delete(mock_booking):
        deleted['booking'] = mock_booking
    monkeypatch.setattr(BookingDao, 'delete', capture_delete)

    result, status = booking_service.BookingService.delete(1)

    assert status == 201
    assert result['message'] == 'Booking deleted successfully'

def test_booking_service_update_success(monkeypatch):
    existing_booking = BookingFactory.build(id=1, quantity=2)

    monkeypatch.setattr(BookingDao, 'fetch_by_id', MagicMock(return_value=existing_booking))
    monkeypatch.setattr(booking_service, 'request', MagicMock(get_json=lambda: {'quantity': 5}))
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(
        dump=lambda b: {'id': b.id, 'quantity': b.quantity},
        load=lambda data: BookingFactory.build(id=data['id'], quantity=data['quantity'])
    ))
    updated = {}
    def update_booking(booking):
        updated['booking'] = booking
    monkeypatch.setattr(BookingDao, 'update', update_booking)

    result, status = booking_service.BookingService.update(1)

    assert status == 200
    assert result['quantity'] == 5

def test_booking_service_update_validation_error(monkeypatch, app_ctx):
    existing_booking = BookingFactory.build(id=1, quantity=2)

    monkeypatch.setattr(BookingDao, 'fetch_by_id', MagicMock(return_value=existing_booking))
    monkeypatch.setattr(booking_service, 'request', MagicMock(get_json=lambda: {'quantity': 'five'}))
    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(
        dump=lambda b: {'id': b.id, 'quantity': b.quantity},
        load=raise_validation
    ))

    result = booking_service.BookingService.update(1)
    assert result.get_json()['status'] == 400

def test_booking_service_update_integrity_error(monkeypatch, app_ctx):
    existing_booking = BookingFactory.build(id=1, product_id=10)

    monkeypatch.setattr(BookingDao, 'fetch_by_id', MagicMock(return_value=existing_booking))
    monkeypatch.setattr(booking_service, 'request', MagicMock(get_json=lambda: {'product_id': 100000}))
    monkeypatch.setattr(booking_service, 'bookingSchema', MagicMock(
        dump=lambda b: {'id': b.id, 'product_id': b.product_id},
        load=lambda data: BookingFactory.build(id=data['id'], product_id=data['product_id'])
    ))

    def raise_integrity(b):
        raise IntegrityError("There is no product with this ID", params=None, orig=None)
    monkeypatch.setattr(BookingDao, 'update', raise_integrity)

    result = booking_service.BookingService.update(1)
    assert result.get_json()['status'] == 400