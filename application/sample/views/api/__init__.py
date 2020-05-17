from __future__ import annotations

import dataclasses
import http
import logging
import traceback
from typing import (
    Any,
    Dict,
    Final,
    cast,
)

import pyramid.request
import pyramid.response

import sample.domain.exceptions as _domain_exceptions
import sample.views.api._converters as _converters
import sample.views.api.exceptions as api_exceptions
import sample.views.api._models as _models


logger: Final = logging.getLogger(__name__)


def _take_json(request: pyramid.request.Request) -> Dict[str, Any]:
    try:
        return cast(Dict[str, Any], request.json)
    except TypeError:  # if Request Body is not JSON
        raise api_exceptions.MissingParameterError()


def sign_in(
        request: pyramid.request.Request) -> pyramid.response.Response:
    parameter: Final = _models.SignIn(**_take_json(request))
    draft_sign_in = _converters.convert_draft_sign_in(parameter)
    try:
        return pyramid.response.Response(
            json=dataclasses.asdict(
                request.domain.authentication.sign_in(draft_sign_in)
            )
        )
    except _domain_exceptions.InvalidCredentialError:
        return pyramid.response.Response(
            json={
                'errors': [
                    {
                        'key': 'all',
                        'message': 'invalid'
                    }
                ]
            },
            status=http.HTTPStatus.BAD_REQUEST,
        )


def sign_up(
        request: pyramid.request.Request) -> pyramid.response.Response:
    parameter: Final = _models.SignUp(**request.json)
    draft_sign_up: Final = _converters.convert_draft_sign_up(parameter)

    try:
        request.domain.authentication.register_user(draft_sign_up)
    except _domain_exceptions.AlreadyRegisteredError:
        return pyramid.response.Response(
            json={
                'errors': [
                    {
                        'key': 'all',
                        'message': 'invalid'
                    }
                ]
            },
            status=http.HTTPStatus.BAD_REQUEST,
        )

    return pyramid.response.Response(status=http.HTTPStatus.CREATED)


def error(
        exception: Exception, request: pyramid.request.Request
) -> pyramid.response.Response:
    logger.debug(
        'reached a view error handler%s %s',
        exception,
        traceback.format_exc()
    )

    logger.exception('reached unexpected error')
    return pyramid.response.Response(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR)
