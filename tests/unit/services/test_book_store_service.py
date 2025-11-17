from unittest.mock import MagicMock
import services.book_store_service as book_store_service
from data_access_objects.book_store_dao import BookStoreDao
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from tests.factories import BookStoreItemFactory

def test_book_store_service_create_success(monkeypatch):
    payload = BookStoreItemFactory.create_payload()

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    book_store_obj = BookStoreItemFactory.build(id=42)
    # Patch the instantiated schema used by the service (bookStoreSchema), not the class
    monkeypatch.setattr(book_store_service, 'bookStoreSchema', MagicMock(load=lambda data: book_store_obj, dump=lambda b: {'id': b.id, 'sold_qty': b.sold_qty}))

    created = {}
    def capture_create(b):
        created['book_store_item'] = b
    monkeypatch.setattr(BookStoreDao, 'create', capture_create)

    result, status = book_store_service.BookStoreService.create()

    assert status == 201
    assert result['sold_qty'] == book_store_obj.sold_qty
    assert 'book_store_item' in created

def test_book_store_service_create_validation_error(monkeypatch, app_ctx):
    payload = BookStoreItemFactory.create_payload()
    payload['sold_qty'] = "invalid_qty"
    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(book_store_service, 'bookStoreSchema', MagicMock(load=raise_validation))

    result = book_store_service.BookStoreService.create()
    assert result.get_json()['status'] == 400

def test_book_store_service_create_integrity_error(monkeypatch, app_ctx): 
    payload = BookStoreItemFactory.create_payload()

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    book_store_obj = BookStoreItemFactory.build(id=42)
    monkeypatch.setattr(book_store_service, 'bookStoreSchema', MagicMock(load=lambda data: book_store_obj))

    def raise_integrity(b):
        raise IntegrityError("Integrity constraint violated", params=None, orig=None)
    monkeypatch.setattr(BookStoreDao, 'create', raise_integrity)

    result = book_store_service.BookStoreService.create()
    assert result.get_json()['status'] == 400

def test_book_store_service_get_all(monkeypatch):
    book_store_items = [
        BookStoreItemFactory.build(id=1),
        BookStoreItemFactory.build(id=2)
    ]

    monkeypatch.setattr(book_store_service, 'bookStoreListSchema',
                        MagicMock(dump=lambda items: [{'id': b.id, 'sold_qty': b.sold_qty} for b in items]))

    monkeypatch.setattr(BookStoreDao, 'fetch_all', lambda: book_store_items)

    result = book_store_service.BookStoreService.get_all()

    assert result == [{'id': 1, 'sold_qty': book_store_items[0].sold_qty},
                      {'id': 2, 'sold_qty': book_store_items[1].sold_qty}]
    
def test_book_store_service_get_by_id(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    monkeypatch.setattr(book_store_service, 'bookStoreSchema',
                        MagicMock(dump=lambda b: {'id': b.id, 'sold_qty': b.sold_qty}))

    monkeypatch.setattr(BookStoreDao, 'fetch_by_id', lambda id: book_store_item)

    result = book_store_service.BookStoreService.get(1)

    assert result == {'id': 1, 'sold_qty': book_store_item.sold_qty}

def test_book_store_service_delete(monkeypatch):
    mock_book_store_item = BookStoreItemFactory.build(id=1)

    monkeypatch.setattr(BookStoreDao, 'fetch_by_id', MagicMock(return_value=mock_book_store_item))
    monkeypatch.setattr(BookStoreDao, 'delete', MagicMock())

    result, status = book_store_service.BookStoreService.delete(1)
    assert result == {'message': 'Book store item deleted successfully'}
    assert status == 201
    BookStoreDao.fetch_by_id.assert_called_once_with(1)
    BookStoreDao.delete.assert_called_once_with(1)

def test_book_store_service_update_success(monkeypatch):
    payload = BookStoreItemFactory.create_payload()
    payload['sold_qty'] = 50

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    book_store_obj = BookStoreItemFactory.build(id=1, sold_qty=20)

    monkeypatch.setattr(book_store_service, 'bookStoreSchema',
                        MagicMock(
                            dump=lambda b: {'id': b.id, 'sold_qty': b.sold_qty},
                            load=lambda data: BookStoreItemFactory.build(id=data['id'], sold_qty=data['sold_qty'])
                        ))

    monkeypatch.setattr(BookStoreDao, 'fetch_by_id', MagicMock(return_value=book_store_obj))
    updated = {}
    def capture_update(b):
        updated['book_store_item'] = b
    monkeypatch.setattr(BookStoreDao, 'update', capture_update)

    result, status = book_store_service.BookStoreService.update(1)

    assert status == 204
    assert result['sold_qty'] == 50
    assert 'book_store_item' in updated
    assert updated['book_store_item'].sold_qty == 50

def test_book_store_service_update_validation_error(monkeypatch, app_ctx):
    exist_book_store_item = BookStoreItemFactory.build(id=1, sold_qty=20)
    monkeypatch.setattr(BookStoreDao, 'fetch_by_id', MagicMock(return_value=exist_book_store_item))
    payload = BookStoreItemFactory.create_payload()
    payload['sold_qty'] = "invalid_qty"

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(book_store_service, 'bookStoreSchema', MagicMock(load=raise_validation))

    result = book_store_service.BookStoreService.update(1)
    assert result.get_json()['status'] == 400

def test_book_store_service_update_integrity_error(monkeypatch, app_ctx):
    payload = BookStoreItemFactory.create_payload()
    payload['sold_qty'] = 100

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(book_store_service, 'request', dummy_request)

    book_store_obj = BookStoreItemFactory.build(id=1, sold_qty=20)

    monkeypatch.setattr(book_store_service, 'bookStoreSchema',
                        MagicMock(
                            dump=lambda b: {'id': b.id, 'sold_qty': b.sold_qty},
                            load=lambda data: BookStoreItemFactory.build(id=data['id'], sold_qty=data['sold_qty'])
                        ))

    monkeypatch.setattr(BookStoreDao, 'fetch_by_id', MagicMock(return_value=book_store_obj))

    def raise_integrity(b):
        raise IntegrityError("Integrity constraint violated", params=None, orig=None)
    monkeypatch.setattr(BookStoreDao, 'update', raise_integrity)

    result = book_store_service.BookStoreService.update(1)
    assert result.get_json()['status'] == 400