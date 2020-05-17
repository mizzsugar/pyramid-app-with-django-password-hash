from __future__ import annotations

import logging
from typing import (
    Final,
)

import sqlalchemy
import sqlalchemy.orm.exc
import sqlalchemy.orm.query
import sqlalchemy.orm.session
import sqlalchemy.exc
import sqlalchemy.sql
import sqlalchemy.sql.expression

import sample.repository._converters as _converters
import sample.repository._definitions as _definitions
import sample.repository.dto as _dto
import sample.repository.exceptions


_migration: Final = _definitions.Migration

_logger: Final = logging.getLogger(__name__)


class Repository:
    def __init__(self, session: sqlalchemy.orm.session.Session) -> None:
        self._session: Final = session
        self.authentication: Final = _Authentication(session)


class _Authentication:
    def __init__(self, session: sqlalchemy.orm.session.Session) -> None:
        self._session: Final = session

    def fetch_by_email(self, email: str) -> _dto.User:
        try:
            return _converters.User.to_dto(
                self._session.query(_definitions.User).
                filter(_definitions.User.email == email).
                one()
            )
        except sqlalchemy.orm.exc.NoResultFound as e:
            raise sample.repository.exceptions.NotFoundError() from e

    def register_user(self, draft: _dto.DraftUser) -> _dto.User:
        user = _definitions.User(email=draft.email, password=draft.password)
        self._session.add(user)

        try:
            self._session.flush()
        except sqlalchemy.exc.IntegrityError:
            raise sample.repository.exceptions.ConflictError()

        return _converters.User.to_dto(user)
