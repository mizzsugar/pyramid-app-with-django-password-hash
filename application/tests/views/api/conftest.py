import unittest.mock

import pyramid.testing
import pytest


@pytest.fixture
def domain():
    return unittest.mock.MagicMock()


@pytest.fixture
def dummy_request(domain):
    request = pyramid.testing.DummyRequest(domain=domain)
    return request
