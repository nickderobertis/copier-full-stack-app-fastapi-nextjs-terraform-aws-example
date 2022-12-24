import pytest
from app.auth.oauth.google.client import get_google_oauth_config
from app.database.engine import get_async_session
from fastapi import FastAPI
from tests.fixtures.google_oauth_config import create_google_oauth_config_stub
from tests.integration.fixtures.db import get_test_async_session, test_db


@pytest.fixture(scope="session")
def test_app(test_db) -> FastAPI:
    from app.app import create_app

    google_config_stub = create_google_oauth_config_stub()
    app = create_app(google_oauth_config=google_config_stub)
    app.dependency_overrides[get_async_session] = get_test_async_session
    app.dependency_overrides[get_google_oauth_config] = lambda: google_config_stub

    yield app
