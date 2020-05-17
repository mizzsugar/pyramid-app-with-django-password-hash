import pytest

import sample.repository.dto
import sample.repository.exceptions


class TestAuthentication:
    def test_register_authentication(
        self,
        repository,
        session,
        count_users,
    ):
        draft = sample.repository.dto.DraftUser(
            email='email@example.com',
            password='password'
        )
        repository.authentication.register_user(draft)
        assert count_users() == 1

    def test_fetch_by_email(
        self,
        repository,
        session,
    ):
        email = 'sample@example.com'
        draft = sample.repository.dto.DraftUser(
            email=email, password='password')
        repository.authentication.register_user(draft)
        actual = repository.authentication.fetch_by_email(email)
        assert actual.email == email

    def test_raise_if_not_registered_email(
        self,
        repository,
        session,
    ):
        email = 'sample@example.com'

        with pytest.raises(sample.repository.exceptions.NotFoundError):
            repository.authentication.fetch_by_email(email)

    def test_authentication_conflict(
        self,
        repository,
        session,
    ):
        draft = sample.repository.dto.DraftUser(
            email='sample@example.com', password='password')
        repository.authentication.register_user(draft)

        with pytest.raises(sample.repository.exceptions.ConflictError):
            repository.authentication.register_user(draft)
