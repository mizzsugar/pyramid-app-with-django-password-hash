from __future__ import annotations

from typing import (
    Final,
)

import sample.domain.dto as _dto
import sample.domain.exceptions as _exceptions
import sample.libs.password as _password
import sample.repository as _repository
import sample.repository.dto as _repository_dto
import sample.repository.exceptions as _repository_exceptions
import sample.domain._converters as _converters


class Authentication:
    def __init__(self, repository: _repository.Repository) -> None:
        self._repository: Final = repository

    def sign_in(self, draft: _dto.SignIn) -> _dto.User:
        try:
            user = self._repository.authentication.fetch_by_email(draft.email)
        except _repository_exceptions.NotFoundError:
            raise _exceptions.InvalidCredentialError()

        if not _password.check_password(draft.password, user.password):
            raise _exceptions.InvalidCredentialError()

        return _converters.User.from_repository(user)

    def register_user(
        self,
        draft: _dto.DraftUser
    ) -> None:
        password = _password.make_password(draft.password)

        try:
            self._repository.authentication.register_user(
                _repository_dto.DraftUser(
                    email=draft.email, password=password)
            )
        except _repository_exceptions.ConflictError:
            raise _exceptions.AlreadyRegisteredError()
