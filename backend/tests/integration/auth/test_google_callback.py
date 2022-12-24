from unittest.mock import patch

import jwt
import pytest
from app.auth.oauth.google.connected_router import ConnectedAccounts
from httpx import AsyncClient
from tests.integration.fixtures.client import *


@pytest.mark.anyio
async def test_user_and_oauth_client_created_on_google_oauth_callback(
    test_client: AsyncClient,
):
    with patch.object(jwt, "decode", return_value={}):
        callback_response = await test_client.get(
            "/auth/google/callback", params=dict(code="code", state="state")
        )
    assert callback_response.status_code == 200
    data = callback_response.json()
    access_token = data["access_token"]

    emails_response = await test_client.get(
        "/auth/connected/google/connected",
        headers=dict(Authorization=f"Bearer {access_token}"),
    )
    connected_accounts = ConnectedAccounts(**emails_response.json())
    assert len(connected_accounts.connected_emails) == 1
