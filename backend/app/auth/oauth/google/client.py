from dataclasses import dataclass
from typing import AsyncGenerator

from app.auth.oauth.google.model import GoogleProfileResponse
from httpx_oauth.clients.google import PROFILE_ENDPOINT, GoogleOAuth2
from logger import log
from settings.google import GOOGLE_SETTINGS, GoogleSettings


class GoogleClientException(Exception):
    pass


class CustomGoogleOAuthClient(GoogleOAuth2):
    async def get_user_info(self, token: str) -> GoogleProfileResponse:
        async with self.get_httpx_client() as client:
            response = await client.get(
                PROFILE_ENDPOINT,
                params={"personFields": "emailAddresses,names"},
                headers={**self.request_headers, "Authorization": f"Bearer {token}"},
            )

            if response.status_code >= 400:
                raise GoogleClientException(response.json())

            data = response.json()
            return GoogleProfileResponse(**data)


@dataclass
class GoogleOAuthConfig:
    client: CustomGoogleOAuthClient
    jwt_secret: str


def create_google_oauth_config(
    settings: GoogleSettings = GOOGLE_SETTINGS,
) -> GoogleOAuthConfig | None:
    if not settings.client_id or not settings.client_secret or not settings.jwt_secret:
        log.warn(
            "Google OAuth2 client not configured. Missing client_id, client_secret, or jwt_secret"
        )
        return None

    log.info("Creating Google OAuth2 client")
    client = CustomGoogleOAuthClient(
        client_id=settings.client_id,
        client_secret=settings.client_secret,
    )
    return GoogleOAuthConfig(client=client, jwt_secret=settings.jwt_secret)


google_oauth_config: GoogleOAuthConfig | None = create_google_oauth_config()


async def get_google_oauth_config() -> AsyncGenerator[GoogleOAuthConfig | None, None]:
    yield google_oauth_config
