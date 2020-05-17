import pytest

import sample.repository
import sample.repository._definitions


@pytest.fixture
def repository(session):
    return sample.repository.Repository(session)


@pytest.fixture
def count_users(session):
    return lambda: session.query(
        sample.repository._definitions.User).count()
