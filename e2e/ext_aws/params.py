import json
import os
from typing import Sequence

import typer
from mypy_boto3_ssm import SSMClient

APP_NAME = os.getenv("APP_NAME")
GLOBAL_APP_NAME = os.getenv("GLOBAL_APP_NAME")


def get_parameters(
    client: SSMClient,
    param_names: Sequence[str],
    app_name: str = APP_NAME,
    param_section: str = "app",
) -> dict[str, str]:
    prefix = create_app_prefix(app_name, param_section)
    return _get_params_for_prefix(client, param_names, prefix)


def get_global_parameters(
    client: SSMClient,
    param_names: Sequence[str],
    global_app_name: str = GLOBAL_APP_NAME,
    param_section: str = "global",
) -> dict[str, str]:
    prefix = create_app_prefix(global_app_name, param_section)
    return _get_params_for_prefix(client, param_names, prefix)


def _get_params_for_prefix(
    client: SSMClient,
    param_names: Sequence[str],
    prefix: str,
) -> dict[str, str]:
    parameters = client.get_parameters(
        Names=[f"{prefix}{param_name}" for param_name in param_names],
        WithDecryption=True,
    )
    return {
        remove_prefix(param["Name"], prefix): param["Value"]
        for param in parameters["Parameters"]
    }


def create_app_prefix(app_name: str, param_section: str) -> str:
    # TODO: parameterize this
    return f"/{app_name}/{param_section}/"


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def main(
    param_names: list[str] = typer.Argument(default=None),
    param_section: str = typer.Option("app"),
) -> None:
    from ext_aws.client import get_client

    client = get_client()
    if not param_names:
        param_names = [
            "SENTRY_ORGANIZATION_SLUG",
            "SENTRY_FE_PROJECT_SLUG",
            "SENTRY_API_PROJECT_SLUG",
        ]
    params = get_parameters(client, param_names, param_section=param_section)
    print(json.dumps(params))


if __name__ == "__main__":
    typer.run(main)
