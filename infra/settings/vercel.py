from pydantic import BaseSettings


class VercelSettings(BaseSettings):
    api_token: str

    class Config:
        env_prefix = "VERCEL_"


VERCEL_SETTINGS = VercelSettings()
