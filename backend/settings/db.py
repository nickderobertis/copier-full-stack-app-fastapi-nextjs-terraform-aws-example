from pydantic import BaseSettings


class DBSettings(BaseSettings):
    host: str = "localhost"
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    type: str = "postgresql"
    driver: str = "asyncpg"

    @property
    def uri(self) -> str:
        uri = f"{self.type}+{self.driver}://{self.user}"
        if self.password:
            uri += ":" + self.password
        return uri + f"@{self.host}/{self.name}"

    class Config:
        env_file = ".env"
        env_prefix = "DB_"


DB_SETTINGS = DBSettings()

if __name__ == "__main__":
    print(DBSettings())
