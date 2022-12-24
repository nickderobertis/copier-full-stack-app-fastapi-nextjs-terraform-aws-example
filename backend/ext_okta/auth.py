from ext_okta.settings import OKTA_SETTINGS, OktaSettings
from okta.client import Client as OktaClient


def create_okta_client(settings: OktaSettings = OKTA_SETTINGS) -> OktaClient:
    if settings.client_log_level is not None:
        log_settings = {
            "logging": {"enabled": True, "level": settings.client_log_level}
        }
    else:
        log_settings = {}

    config = {
        "orgUrl": settings.org_url,
        "authorizationMode": "PrivateKey",
        "clientId": settings.client_id,
        "scopes": ["okta.logs.read"],
        "privateKey": settings.private_key,  # this parameter should be type of str
        **log_settings,
    }
    return OktaClient(config)
