from pydantic import BaseSettings


class SentrySettings(BaseSettings):
    auth_token: str
    organization_slug: str

    class Config:
        env_prefix = "SENTRY_"


SENTRY_SETTINGS = SentrySettings()
