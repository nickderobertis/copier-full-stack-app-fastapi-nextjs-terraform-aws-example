import datetime
from typing import Tuple

from app.auth.oauth.google.client import CustomGoogleOAuthClient
from app.auth.oauth.google.model import GoogleProfileResponse
from httpx_oauth.oauth2 import OAuth2Token
from pydantic_factories import ModelFactory


class GoogleProfileResponseFactory(ModelFactory):
    __model__ = GoogleProfileResponse


class GoogleOAuthClientStub(CustomGoogleOAuthClient):
    async def get_user_info(self, token: str) -> GoogleProfileResponse:
        return GoogleProfileResponseFactory.build()

    async def get_id_email(self, token: str) -> Tuple[str, str]:
        return "123", "abc@123.com"

    async def get_access_token(
        self, code: str, redirect_uri: str, code_verifier: str = None
    ) -> OAuth2Token:
        five_minutes_from_now = datetime.datetime.now() + datetime.timedelta(minutes=5)
        five_minutes_from_now_epoch = int(five_minutes_from_now.timestamp())
        return OAuth2Token(
            dict(access_token="access_token", expires_at=five_minutes_from_now_epoch)
        )
