import os
import pytest

from application import create_app
from application import db as _db


TEST_DATABASE_URI = os.getenv(
    'TEST_DATABASE_URI', 
    'postgresql+psycopg2://tester:12345@localhost:6666/flaskdb_test'
    )



@pytest.fixture(scope='session')
def app(request):
    """ Session wide test 'Flask' application """
    settings_override = {
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,

        'SQLALCHEMY_DATABASE_URI': TEST_DATABASE_URI
    }

    app = create_app('local', settings_override)
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture(scope='function')
def db(app):
    """ Session-wide test database """
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db
    
    _db.session.close()
    _db.drop_all()
 
