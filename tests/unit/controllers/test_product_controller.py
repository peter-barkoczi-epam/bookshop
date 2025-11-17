import controllers.product_controller as product_controller

from schemas.product_schema import ProductSchema
from tests.factories import ProductFactory
from unittest.mock import MagicMock


def test_get_all_products_unit(monkeypatch):
    products = [
        ProductFactory.build(id=1),
        ProductFactory.build(id=2)
    ]
    product_list_schema = ProductSchema(many=True)
    mock_products = product_list_schema.dump(products)

    mock_service = MagicMock()
    mock_service.get_all.return_value = mock_products

    monkeypatch.setattr(product_controller, 'ProductService', mock_service)

    result = product_controller.ProductController.get_all()

    assert result == mock_products
    mock_service.get_all.assert_called_once()

def test_get_product_by_id_unit(monkeypatch):
    user = ProductFactory.build(id=1)
    
    product_schema = ProductSchema()
    mock_user = product_schema.dump(user)

    mock_service = MagicMock()
    mock_service.get.return_value = mock_user

    monkeypatch.setattr(product_controller, 'ProductService', mock_service)

    result = product_controller.ProductController.get(1)

    assert result == mock_user
    mock_service.get.assert_called_once_with(1)

def test_create_product_unit(monkeypatch):
    user = ProductFactory.build(id=1)

    user_schema = ProductSchema()
    mock_user = user_schema.dump(user)

    mock_service = MagicMock()
    mock_service.create.return_value = (mock_user, 201)

    monkeypatch.setattr(product_controller, 'ProductService', mock_service)

    result = product_controller.ProductController.create()
    assert result == (mock_user, 201)
    mock_service.create.assert_called_once_with()

def test_delete_product_unit(monkeypatch):
    mock_service = MagicMock()
    mock_service.delete.return_value = ('Product deleted successfully', 201)

    monkeypatch.setattr(product_controller, 'ProductService', mock_service)

    result = product_controller.ProductController.delete(1)
    assert result == ('Product deleted successfully', 201)
    mock_service.delete.assert_called_once_with(1)

def test_update_product_unit(monkeypatch):
    user = ProductFactory.build(id=1)

    user_schema = ProductSchema()
    mock_user = user_schema.dump(user)

    mock_service = MagicMock()
    mock_service.update.return_value = (mock_user, 200)

    monkeypatch.setattr(product_controller, 'ProductService', mock_service)

    result = product_controller.ProductController.update(1)
    assert result == (mock_user, 200)
    mock_service.update.assert_called_once_with(1)