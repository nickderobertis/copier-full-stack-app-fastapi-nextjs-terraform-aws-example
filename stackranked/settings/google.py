from pydantic import BaseSettings


class GoogleSettings(BaseSettings):
    client_id: str | None = None
    client_secret: str | None = None
    jwt_secret: str | None = None

    class Config:
        env_file = ".env"
        env_prefix = "GOOGLE_"


GOOGLE_SETTINGS = GoogleSettings()

if __name__ == "__main__":
    print(GOOGLE_SETTINGS)
