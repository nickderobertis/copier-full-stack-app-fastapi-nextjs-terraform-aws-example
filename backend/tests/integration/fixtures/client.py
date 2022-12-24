import pytest
from httpx import AsyncClient
from tests.integration.fixtures.app import *


@pytest.fixture(scope="session")
async def test_client(test_app) -> AsyncClient:
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac
