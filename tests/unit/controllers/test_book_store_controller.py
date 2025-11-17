import controllers.book_store_controller as book_store_controller

from schemas.store_item_schema import BookStoreItemSchema
from tests.factories import BookStoreItemFactory
from unittest.mock import MagicMock


def test_get_all_book_store_items_unit(monkeypatch):
    book_store_items = [
        BookStoreItemFactory.build(id=1),
        BookStoreItemFactory.build(id=2)
    ]
    book_store_item_list_schema = BookStoreItemSchema(many=True)
    mock_items = book_store_item_list_schema.dump(book_store_items)

    mock_service = MagicMock()
    mock_service.get_all.return_value = mock_items

    monkeypatch.setattr(book_store_controller, 'BookStoreService', mock_service)

    result = book_store_controller.BookStoreController.get_all()

    assert result == mock_items
    mock_service.get_all.assert_called_once()

def test_get_book_store_item_by_id_unit(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)
    
    book_store_item_schema = BookStoreItemSchema()
    mock_book_store_item = book_store_item_schema.dump(book_store_item)

    mock_service = MagicMock()
    mock_service.get.return_value = mock_book_store_item

    monkeypatch.setattr(book_store_controller, 'BookStoreService', mock_service)

    result = book_store_controller.BookStoreController.get(1)

    assert result == mock_book_store_item
    mock_service.get.assert_called_once_with(1)

def test_create_book_store_item_unit(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    book_store_item_schema = BookStoreItemSchema()
    mock_book_store_item = book_store_item_schema.dump(book_store_item)

    mock_service = MagicMock()
    mock_service.create.return_value = (mock_book_store_item, 201)

    monkeypatch.setattr(book_store_controller, 'BookStoreService', mock_service)

    result = book_store_controller.BookStoreController.create()
    assert result == (mock_book_store_item, 201)
    mock_service.create.assert_called_once_with()

def test_delete_book_store_item_unit(monkeypatch):
    mock_service = MagicMock()
    mock_service.delete.return_value = ('Book Store item deleted successfully', 201)

    monkeypatch.setattr(book_store_controller, 'BookStoreService', mock_service)

    result = book_store_controller.BookStoreController.delete(1)
    assert result == ('Book Store item deleted successfully', 201)
    mock_service.delete.assert_called_once_with(1)

def test_update_book_store_item_unit(monkeypatch):
    book_store_item = BookStoreItemFactory.build(id=1)

    book_store_item_schema = BookStoreItemSchema()
    mock_book_store_item = book_store_item_schema.dump(book_store_item)

    mock_service = MagicMock()
    mock_service.update.return_value = (mock_book_store_item, 200)

    monkeypatch.setattr(book_store_controller, 'BookStoreService', mock_service)

    result = book_store_controller.BookStoreController.update(1)
    assert result == (mock_book_store_item, 200)
    mock_service.update.assert_called_once_with(1)