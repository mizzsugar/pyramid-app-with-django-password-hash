from __future__ import annotations

from typing import (
    Callable,
    Final,
)

import pyramid.config
import pyramid.registry
import pyramid.request
import pyramid.response
import zope.sqlalchemy

import sample.application
import sample.bootstrap
import sample.domain
import sample.repository


_VIEW = Callable[[pyramid.request.Request], pyramid.response.Response]


def _init_repository(config: pyramid.config.Configurator) -> None:
    settings: Final = config.get_settings()
    settings['tm.manager_hook'] = 'pyramid_tm.explicit_manager'

    config.include('pyramid_tm')
    session_factory = sample.bootstrap.sqlalchemy_session_factory_factory()

    def request_method(
            request: pyramid.request.Request
    ) -> sample.repository.Repository:
        session: Final = session_factory()
        zope.sqlalchemy.register(session, transaction_manager=request.tm)
        return sample.repository.Repository(session)

    config.add_request_method(request_method, 'repository', reify=True)


def _init_domain(config: pyramid.config.Configurator) -> None:
    settings: Final = config.get_settings()
    domain_factory: Final = sample.bootstrap.domain_factory(settings)

    def request_method(
            request: pyramid.request.Request
    ) -> sample.domain.Domain:
        return domain_factory(request.repository)

    config.add_request_method(request_method, 'domain', reify=True)


def main() -> pyramid.router.Router:
    """ This function returns a Pyramid WSGI application.
    """
    settings: Final = sample.application.settings()
    with pyramid.config.Configurator(settings=settings) as config:
        config.include('.views.routes')
        _init_repository(config)
        _init_domain(config)
        return config.make_wsgi_app()
