from __future__ import annotations

import contextlib
from typing import (
    Callable,
    Final,
    Iterator,
)
import sqlalchemy
import sqlalchemy.orm

import sample.application
import sample.bootstrap
import sample.domain
import sample.repository


def sqlalchemy_session_factory_factory() -> sqlalchemy.orm.sessionmaker:
    engine: Final = sqlalchemy.create_engine(
        'sqlite:///db.sqlite3', echo=False)
    session_factory: Final = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=engine)

    return session_factory


def domain_factory(
        settings: sample.application.Settings
) -> Callable[
    [sample.repository.Repository], sample.domain.Domain
]:
    def f(
            repository: sample.repository.Repository
    ) -> sample.domain.Domain:
        return sample.domain.Domain(repository=repository)

    return f


@contextlib.contextmanager
def domain(
        settings: sample.application.Settings,
) -> Iterator[sample.domain.Domain]:
    domain_factory: Final = sample.bootstrap.domain_factory(settings)
    session: Final = sample.bootstrap.sqlalchemy_session_factory_factory()()
    try:
        yield domain_factory(sample.repository.Repository(session))
        session.commit()
    finally:
        session.close()
