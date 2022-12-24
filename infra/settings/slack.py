from pydantic import BaseSettings


class SlackSettings(BaseSettings):
    token: str
    webhook_url: str

    class Config:
        env_prefix = "SLACK_"


SLACK_SETTINGS = SlackSettings()
