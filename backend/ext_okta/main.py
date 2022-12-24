import asyncio

from ext_okta.auth import create_okta_client
from ext_okta.get_logs import get_logs
from ext_okta.settings import OKTA_SETTINGS, OktaSettings
from okta.models import LogEvent


def get_user_login_events(
    max_results: int | None = None,
    settings: OktaSettings = OKTA_SETTINGS,
) -> list[LogEvent]:
    client = create_okta_client(settings=settings)
    logs = asyncio.run(get_logs(client, max_results=max_results))

    return logs


if __name__ == "__main__":
    max_results = 5
    print(get_user_login_events(max_results=max_results))
