import pytest

from app import app, CURRENT


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
    with app.test_client() as test_client:
        yield test_client
    CURRENT['puzzle'] = None
    CURRENT['solution'] = None
