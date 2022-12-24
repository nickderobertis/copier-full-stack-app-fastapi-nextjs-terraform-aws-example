import asyncio
import json
from pathlib import Path

from ext_google.auth import login_get_credentials
from ext_google.reports.query.login import query_login_reports
from ext_google.reports.query.tokens import query_token_authorization
from ext_google.reports.service import create_reports_service
from ext_okta.auth import create_okta_client
from ext_okta.get_logs import get_logs
from okta.models import LogEvent
from tests.config import (
    GOOGLE_LOGIN_RESPONSE_PATH,
    GOOGLE_TOKEN_RESPONSE_PATH,
    OKTA_LOGIN_RESPONSE_PATH,
)


def generate_google_login_response_json(
    out_path: Path = GOOGLE_LOGIN_RESPONSE_PATH, max_res: int = 5
) -> None:
    creds = login_get_credentials()
    service = create_reports_service(creds)
    activities = query_login_reports(service, max_results=max_res)
    json_str = json.dumps(activities, indent=2)
    out_path.write_text(json_str)


def generate_google_token_response_json(
    out_path: Path = GOOGLE_TOKEN_RESPONSE_PATH, max_res: int = 5
) -> None:
    creds = login_get_credentials()
    service = create_reports_service(creds)
    activities = list(query_token_authorization(service, max_results=max_res))
    json_str = json.dumps(activities, indent=2)
    out_path.write_text(json_str)


def generate_okta_login_response_json(
    out_path: Path = OKTA_LOGIN_RESPONSE_PATH,
) -> None:
    async def create_logs(max_results: int) -> list[LogEvent]:
        client = create_okta_client()
        logs = await get_logs(client, max_results=max_results)
        return logs

    max_results = 5
    logs = asyncio.run(create_logs(max_results=max_results))
    data = [log.as_dict() for log in logs]
    data_str = json.dumps(data, indent=2)
    out_path.write_text(data_str)


if __name__ == "__main__":
    generate_google_login_response_json()
    generate_google_token_response_json()
    generate_okta_login_response_json()
