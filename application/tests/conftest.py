import pytest
import sqlalchemy
import zope.sqlalchemy

import sample.application
import sample.scripts.database


@pytest.fixture(scope='session')
def _sqlite_setting():
    return 'sqlite:///test.sqlite3'


@pytest.fixture(scope='session')
def _recreate_database():
    sample.scripts.database._recreate(
        'test.sqlite3', quiet=True, migrate=True)


@pytest.fixture(scope='session')
def session_factory(_recreate_database, _sqlite_setting):
    engine = sqlalchemy.create_engine(_sqlite_setting, echo=False)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=engine)

    return session_factory


@pytest.fixture()
def session(session_factory):
    session = session_factory()
    zope.sqlalchemy.register(session)

    yield session
    session.close()
