from unittest.mock import MagicMock
import services.product_service as product_service
from data_access_objects.product_dao import ProductDao
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from tests.factories import ProductFactory

def test_product_service_create_success(monkeypatch):
    payload = ProductFactory.create_payload()

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    product_obj = ProductFactory.build(id=42)
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(load=lambda data: product_obj, dump=lambda p: {'id': p.id, 'name': p.name}))

    created = {}
    def capture_create(p):
        created['product'] = p
    monkeypatch.setattr(ProductDao, 'create', capture_create)

    result, status = product_service.ProductService.create()

    assert status == 201
    assert result['name'] == product_obj.name
    assert 'product' in created

def test_product_service_create_validation_error(monkeypatch, app_ctx):
    payload = ProductFactory.create_payload()
    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(load=raise_validation))

    result = product_service.ProductService.create()
    assert result.get_json()['status'] == 400

def test_product_service_create_integrity_error(monkeypatch, app_ctx): 
    payload = ProductFactory.create_payload(price="9.99")

    dummy_request = MagicMock(get_json=lambda: payload)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    product_obj = ProductFactory.build(id=42)
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(load=lambda data: product_obj))

    def raise_integrity(p):
        raise IntegrityError("Invalid format", params=None, orig=None)
    monkeypatch.setattr(ProductDao, 'create', raise_integrity)

    result = product_service.ProductService.create()
    assert result.get_json()['status'] == 400

def test_product_service_get_all(monkeypatch):
    products = [
        ProductFactory.build(id=1),
        ProductFactory.build(id=2)
    ]
    dumped_products = [ProductFactory.dump(p) for p in products]

    monkeypatch.setattr(ProductDao, 'fetch_all', MagicMock(return_value=products))
    monkeypatch.setattr(product_service, 'productListSchema', MagicMock(dump=MagicMock(return_value=dumped_products)))

    result = product_service.ProductService.get_all()

    assert result == dumped_products
    ProductDao.fetch_all.assert_called_once()
    product_service.productListSchema.dump.assert_called_once_with(products)

def test_product_service_get(monkeypatch):  
    product = ProductFactory.build(id=1)
    dumped_product = ProductFactory.dump(product)

    monkeypatch.setattr(ProductDao, 'fetch_by_id', MagicMock(return_value=product))
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(dump=MagicMock(return_value=dumped_product)))

    result = product_service.ProductService.get(1)

    assert result == dumped_product
    ProductDao.fetch_by_id.assert_called_once_with(1)
    product_service.productSchema.dump.assert_called_once_with(product)

def test_product_service_delete(monkeypatch):
    product = ProductFactory.build(id=1)

    monkeypatch.setattr(ProductDao, 'fetch_by_id', MagicMock(return_value=product))
    monkeypatch.setattr(ProductDao, 'delete', MagicMock())

    result, status = product_service.ProductService.delete(1)

    assert status == 201
    assert result['message'] == 'Product deleted successfully'
    ProductDao.fetch_by_id.assert_called_once_with(1)
    ProductDao.delete.assert_called_once_with(1)

def test_product_service_update_success(monkeypatch):
    product = ProductFactory.build(id=1)
    updated_data = {'name': 'Updated Product', 'price': 19.99}
    updated_product = ProductFactory.build(id=1, **updated_data)
    dumped_updated_product = ProductFactory.dump(updated_product)

    dummy_request = MagicMock(get_json=lambda: updated_data)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    monkeypatch.setattr(ProductDao, 'fetch_by_id', MagicMock(return_value=product))
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(
        dump=MagicMock(side_effect=lambda p: ProductFactory.dump(p)),
        load=MagicMock(side_effect=lambda data: updated_product)
    ))
    monkeypatch.setattr(ProductDao, 'update', MagicMock())

    result, status = product_service.ProductService.update(1)

    assert status == 200
    assert result == dumped_updated_product
    ProductDao.fetch_by_id.assert_called_once_with(1)
    product_service.productSchema.dump.assert_called()
    product_service.productSchema.load.assert_called()
    ProductDao.update.assert_called_once_with(updated_product)

def test_product_service_update_validation_error(monkeypatch, app_ctx):
    product = ProductFactory.build(id=1)
    invalid_data = {'name': '', 'price': -10}

    dummy_request = MagicMock(get_json=lambda: invalid_data)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    monkeypatch.setattr(ProductDao, 'fetch_by_id', MagicMock(return_value=product))

    def raise_validation(data):
        raise ValidationError("Invalid data")
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(
        dump=MagicMock(side_effect=lambda p: ProductFactory.dump(p)),
        load=raise_validation
    ))

    result = product_service.ProductService.update(1)
    assert result.get_json()['status'] == 400

def test_product_service_update_integrity_error(monkeypatch, app_ctx):
    product = ProductFactory.build(id=1)
    conflicting_data = {'name': 'Existing Product', 'price': 29.99}

    dummy_request = MagicMock(get_json=lambda: conflicting_data)
    monkeypatch.setattr(product_service, 'request', dummy_request)

    monkeypatch.setattr(ProductDao, 'fetch_by_id', MagicMock(return_value=product))

    def raise_integrity(data):
        raise IntegrityError("Duplicate entry", params=None, orig=None)
    monkeypatch.setattr(product_service, 'productSchema', MagicMock(
        dump=MagicMock(side_effect=lambda p: ProductFactory.dump(p)),
        load=raise_integrity
    ))

    result = product_service.ProductService.update(1)
    assert result.get_json()['status'] == 400