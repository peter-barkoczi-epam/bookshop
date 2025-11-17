from unittest.mock import MagicMock
from types import SimpleNamespace

from data_access_objects.product_dao import ProductDao
from models.products_model import Product
from tests.factories import ProductFactory
from app import app as flask_app


def test_fetch_by_id_returns_product(monkeypatch):
    product = ProductFactory.build(id=1)

    mock_query = MagicMock()
    mock_query.get_or_404.return_value = product

    with flask_app.app_context():
        monkeypatch.setattr(Product, 'query', mock_query, raising=False)

    result = ProductDao.fetch_by_id(1)

    assert result == product
    mock_query.get_or_404.assert_called_once_with(1, description=ProductDao.PRODUCT_NOT_FOUND.format(1))


def test_fetch_all_returns_list(monkeypatch):
    products = [ProductFactory.build(id=1), ProductFactory.build(id=2)]
    mock_query = MagicMock()
    mock_query.all.return_value = products
    with flask_app.app_context():
        monkeypatch.setattr(Product, 'query', mock_query, raising=False)

    result = ProductDao.fetch_all()

    assert result == products
    mock_query.all.assert_called_once()


def test_create_calls_session_add_and_commit(monkeypatch):
    product = ProductFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.product_dao.db', db_mock)

    ProductDao.create(product)

    session.add.assert_called_once_with(product)
    session.commit.assert_called_once()


def test_delete_fetches_and_deletes_item(monkeypatch):
    product = ProductFactory.build(id=1)

    mock_filter = MagicMock()
    mock_filter.first.return_value = product

    mock_query = MagicMock()
    mock_query.filter_by.return_value = mock_filter
    with flask_app.app_context():
        monkeypatch.setattr(Product, 'query', mock_query, raising=False)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.product_dao.db', db_mock)

    ProductDao.delete(1)

    mock_query.filter_by.assert_called_once_with(id=1)
    session.delete.assert_called_once_with(product)
    session.commit.assert_called_once()


def test_update_calls_merge_and_commit(monkeypatch):
    product = ProductFactory.build(id=1)

    session = MagicMock()
    db_mock = SimpleNamespace(session=session)
    monkeypatch.setattr('data_access_objects.product_dao.db', db_mock)

    ProductDao.update(product)

    session.merge.assert_called_once_with(product)
    session.commit.assert_called_once()