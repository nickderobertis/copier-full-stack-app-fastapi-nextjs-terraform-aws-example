from app.auth.oauth.google.client import GoogleOAuthConfig
from tests.fixtures.google_oauth_client_stub import GoogleOAuthClientStub


def create_google_oauth_config_stub() -> GoogleOAuthConfig:
    return GoogleOAuthConfig(
        client=GoogleOAuthClientStub(
            client_id="client_id", client_secret="client_secret"
        ),
        jwt_secret="secret",
    )
