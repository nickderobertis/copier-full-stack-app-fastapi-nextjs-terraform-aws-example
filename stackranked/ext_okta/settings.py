from pathlib import Path

from pydantic import BaseSettings


class OktaSettings(BaseSettings):
    client_id: str
    org_url: str
    client_log_level: int | None = None

    class Config:
        env_file = ".env"
        env_prefix = "OKTA_"

    @property
    def private_key(self) -> str:
        return Path("okta-keypair.json").read_text()


OKTA_SETTINGS = OktaSettings()

if __name__ == "__main__":
    print(OKTA_SETTINGS)
