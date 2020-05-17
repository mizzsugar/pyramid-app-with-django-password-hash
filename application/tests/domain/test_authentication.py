import unittest.mock

import pytest

import sample.domain.authentication
import sample.domain.dto
import sample.domain.exceptions
import sample.repository.dto
import sample.repository.exceptions


@pytest.fixture
def authentication_domain():
    def f(
        repository=unittest.mock.MagicMock()
    ):
        return sample.domain.authentication.Authentication(
            repository=repository)

    return f


@unittest.mock.patch('sample.libs.password.check_password')
def test_sign_in(mock_check_password, authentication_domain):
    user_id = 1
    email = 'sample@example.com'
    mock_repository = unittest.mock.MagicMock()
    mock_repository.authentication.fetch_by_email.return_value =\
        sample.repository.dto.User(
            id=user_id, email=email, password='password')
    mock_check_password.return_value = True

    domain = authentication_domain(repository=mock_repository)

    draft = sample.domain.dto.SignIn(email=email, password='password')

    expected = sample.domain.dto.User(id=user_id, email=email)

    actual = domain.sign_in(draft)

    assert actual == expected


@unittest.mock.patch('sample.libs.password.check_password')
def test_cannot_sign_in_if_failed_checking_password(
        mock_check_password, authentication_domain):
    email = 'sample@example.com'
    mock_repository = unittest.mock.MagicMock()
    mock_repository.authentication.fetch_by_email.return_value =\
        sample.repository.dto.User(id=1, email=email, password='password')
    mock_check_password.return_value = False

    domain = authentication_domain(repository=mock_repository)

    draft = sample.domain.dto.SignIn(email=email, password='password')

    with pytest.raises(sample.domain.exceptions.InvalidCredentialError):
        domain.sign_in(draft)


@unittest.mock.patch('sample.libs.password.make_password')
def test_sign_up(mock_hash_password, authentication_domain):
    email = 'sample@example.com'
    password = 'password'
    mock_hash_password.return_value = 'hashed_password'
    mock_repository = unittest.mock.MagicMock()
    mock_repository.authentication.register_user.return_value =\
        sample.repository.dto.User(
            id=1, email=email, password=password)

    domain = authentication_domain(repository=mock_repository)

    draft = sample.domain.dto.DraftUser(email=email, password=password)

    domain.register_user(draft)
    mock_hash_password.assert_called_once_with(password)


def test_cannot_sign_up_if_email_is_already_used(authentication_domain):
    email = 'sample@example.com'
    mock_repository = unittest.mock.MagicMock()
    mock_repository.authentication.register_user.side_effect =\
        sample.repository.exceptions.ConflictError
    domain = authentication_domain(repository=mock_repository)

    draft = sample.domain.dto.DraftUser(email=email, password='password')

    with pytest.raises(sample.domain.exceptions.AlreadyRegisteredError):
        domain.register_user(draft)
