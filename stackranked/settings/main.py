from typing import Optional

from pydantic import BaseSettings
from settings.db import DB_SETTINGS, DBSettings
from settings.environment import EnvironmentType
from settings.google import GOOGLE_SETTINGS, GoogleSettings


class Settings(BaseSettings):
    fe_url: str
    email_user: str
    email_password: str

    sentry_dsn: Optional[str] = None

    db: DBSettings = DB_SETTINGS
    google: GoogleSettings = GOOGLE_SETTINGS
    environment_type: EnvironmentType = EnvironmentType.DEVELOPMENT
    sql_echo: bool = False
    log_level: str = "INFO"
    enable_dev_endpoints: bool = False

    class Config:
        env_file = ".env"


SETTINGS = Settings()

if __name__ == "__main__":
    print(SETTINGS)
