from pydantic import BaseSettings


class GoogleSettings(BaseSettings):
    default_retries: int = 5

    class Config:
        env_file = ".env"
        env_prefix = "GOOGLE_"


GOOGLE_SETTINGS = GoogleSettings()

if __name__ == "__main__":
    print(GOOGLE_SETTINGS)
