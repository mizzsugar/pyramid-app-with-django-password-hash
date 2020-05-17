import http

import sample.domain.dto
import sample.domain.exceptions
import sample.views.api


def test_sign_in(domain, dummy_request):
    user_id = 1
    email = 'email@example.com'
    dummy_request.json = {'email': email, 'password': 'password'}
    dummy_request.domain.authentication.sign_in.return_value =\
        sample.domain.dto.User(
            id=user_id, email=email)
    response = sample.views.api.sign_in(dummy_request)
    assert response.status_code == http.HTTPStatus.OK
    assert response.json['id'] == user_id
    assert response.json['email'] == email


def test_fail_sign_in(domain, dummy_request):
    email = 'email@example.com'
    dummy_request.json = {'email': email, 'password': 'password'}
    dummy_request.domain.authentication.sign_in.side_effect =\
        sample.domain.exceptions.InvalidCredentialError
    response = sample.views.api.sign_in(dummy_request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json['errors'][0]['key'] == 'all'
    assert response.json['errors'][0]['message'] == 'invalid'


def test_sign_up(domain, dummy_request):
    email = 'email@example.com'
    dummy_request.json = {'email': email, 'password': 'password'}
    dummy_request.domain.authentication.register_user.return_value = None
    response = sample.views.api.sign_up(dummy_request)
    assert response.status_code == http.HTTPStatus.CREATED


def test_fail_sign_up(domain, dummy_request):
    email = 'email@example.com'
    dummy_request.json = {'email': email, 'password': 'password'}
    dummy_request.domain.authentication.register_user.side_effect =\
        sample.domain.exceptions.AlreadyRegisteredError
    response = sample.views.api.sign_up(dummy_request)
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
    assert response.json['errors'][0]['key'] == 'all'
    assert response.json['errors'][0]['message'] == 'invalid'
