import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ['ENV'] = 'TESTING'

import pytest
from app import create_app
import base64


@pytest.fixture(scope="session")
def app():
    return create_app()


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        yield


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_header():
    def _auth_header(login, password):
        token = base64.b64encode(f"{login}:{password}".encode()).decode()
        return {"Authorization": f"Basic {token}"}

    return _auth_header
    
@pytest.fixture
def db(app_ctx):
    from database import db as _db
    _db.drop_all()
    if _db.engine.dialect.name == "sqlite":
        from sqlalchemy import text
        from sqlalchemy.exc import OperationalError
        try:
            _db.session.execute(text("DELETE FROM sqlite_sequence"))
            _db.session.commit()
        except OperationalError:
            pass
    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture(autouse=True)
def db_transaction(app_ctx, db):

    from database import db as _db
    from sqlalchemy.orm import scoped_session, sessionmaker
    from sqlalchemy import event

    connection = _db.engine.connect()
    transaction = connection.begin()

    session_factory = sessionmaker(bind=connection)
    session = scoped_session(session_factory)
    old_session = _db.session
    _db.session = session

    session().begin_nested()

    @event.listens_for(session(), "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent:
            sess.begin_nested()

    try:
        yield
    finally:
        session.remove()
        _db.session = old_session
        transaction.rollback()
        connection.close()
