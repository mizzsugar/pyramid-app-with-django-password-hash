import pyramid.config

import sample.views.api as api


def includeme(config: pyramid.config.Configurator) -> None:
    for pattern, view, request_method in [
        ('/api/sign_in', api.sign_in, 'POST'),
        ('/api/sign_up', api.sign_up, 'POST'),
    ]:
        config.add_route(pattern, pattern, request_method=request_method)
        config.add_view(
            view, route_name=pattern, request_method=request_method)

    config.add_view(api.error, context=Exception)
