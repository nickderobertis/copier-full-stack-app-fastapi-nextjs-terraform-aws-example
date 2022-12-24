from pydantic import BaseSettings


class AppSettings(BaseSettings):
    short_name: str
    staging_name_suffix: str

    email_user: str
    email_password: str

    class Config:
        env_prefix = "APP_"


APP_SETTINGS = AppSettings()
