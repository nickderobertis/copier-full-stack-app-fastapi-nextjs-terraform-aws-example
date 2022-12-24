from pydantic import BaseSettings


class NetworkSettings(BaseSettings):
    domain_name: str
    staging_subdomain: str
    health_check_interval: int

    class Config:
        env_prefix = "NETWORK_"


NETWORK_SETTINGS = NetworkSettings()
