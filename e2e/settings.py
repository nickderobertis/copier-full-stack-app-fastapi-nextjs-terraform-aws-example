import os
from typing import Final, Tuple

from ext_aws.client import get_client, get_global_client
from ext_aws.params import get_global_parameters, get_parameters
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable

APP_SSM_PARAMS: Final[list[str]] = [
    "SENTRY_AUTH_TOKEN",
    "SENTRY_ORGANIZATION_SLUG",
    "SENTRY_FE_PROJECT_SLUG",
    "SENTRY_API_PROJECT_SLUG",
    "FE_URL",
    "API_URL",
    "MONITORING_URL",
]

MONITORING_SSM_PARAMS: Final[list[str]] = [
    "GRAFANA_PASSWORD",
]

GLOBAL_SSM_PARAMS: Final[list[str]] = [
    "E2E_GOOGLE_USER",
    "E2E_GOOGLE_PASSWORD",
]

SSM_PARAM_TO_SETTINGS_KEY: Final[dict[str, str]] = dict(
    FE_URL="url",
    MONITORING_URL="grafana_url",
    E2E_GOOGLE_USER="google_user",
    E2E_GOOGLE_PASSWORD="google_password",
)


class Settings(BaseSettings):
    url: str
    api_url: str
    google_user: str
    google_password: str
    grafana_url: str
    grafana_password: str
    rapid_api_key: str
    sentry_auth_token: str
    sentry_organization_slug: str
    sentry_fe_project_slug: str
    sentry_api_project_slug: str

    enable_dev_only_tests: bool = True

    class Config:
        env_file = ".env"
        env_prefix = "E2E_"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            client = get_client()
            global_client = get_global_client()

            def ssm_settings(settings: BaseSettings) -> dict[str, str]:
                params = {
                    **get_global_parameters(global_client, GLOBAL_SSM_PARAMS),
                    **get_parameters(client, APP_SSM_PARAMS),
                    **get_parameters(
                        client, MONITORING_SSM_PARAMS, param_section="monitoring"
                    ),
                }
                params_for_settings = {
                    SSM_PARAM_TO_SETTINGS_KEY.get(key, key).lower(): value
                    for key, value in params.items()
                }
                return params_for_settings

            # Add in SSM params below environment priority
            return init_settings, env_settings, ssm_settings, file_secret_settings


SETTINGS = Settings()

print(
    f"Settings loaded with\n\turl={SETTINGS.url}\n\tapi_url={SETTINGS.api_url}\n\tAPP_NAME={os.getenv('APP_NAME', '')}\n\tenable_dev_only_tests={SETTINGS.enable_dev_only_tests}"
)

if __name__ == "__main__":
    print(SETTINGS)
