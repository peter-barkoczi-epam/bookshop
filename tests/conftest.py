import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ['ENV'] = 'TESTING'

import pytest
from app import create_app


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    return app.test_client()
