import asyncio
import datetime
import json
from typing import AsyncIterator, Dict

from ext_okta.dates import datetime_to_utc_iso
from ext_okta.exc import OktaHTTPException
from ext_okta.ext_response import log_next_request, log_response
from okta.api_response import OktaAPIResponse
from okta.client import Client
from okta.models import LogEvent

last_url: str | None = None


def _should_request_again(resp: OktaAPIResponse) -> bool:
    global last_url

    if not resp.has_next():
        # Use the client built-in behavior. No more next link, stop
        return False
    if last_url is None:
        # Cannot compare against last_url as it is the first check. Simply
        # set last_url and return the client built-in behavior
        last_url = resp._next
        return resp.has_next()
    # Work around the bug in okta/okta-sdk-python#231
    # For some reason, it stops changing the URL and yet continues to say has_next
    if last_url == resp._next:
        # URL is the same, stop
        return False
    last_url = resp._next
    return True


async def iter_logs(
    client: Client,
    max_results: int | None = None,
    since: datetime.datetime | None = None,
) -> AsyncIterator[LogEvent]:
    params: Dict[str, str | int] = dict(
        filter='eventType eq "user.authentication.sso"',
    )
    if max_results is not None:
        params["limit"] = max_results
    if since is not None:
        params["since"] = datetime_to_utc_iso(since)
    logs: list[LogEvent]
    resp: OktaAPIResponse
    logs, resp, err = await client.get_logs(params)
    log_response(resp, 1)
    idx = 2
    while True:
        # Handle response
        if err is not None or logs is None:
            raise OktaHTTPException(err)
        for log in logs:
            yield log

        # Paginate
        if _should_request_again(resp):
            log_next_request(resp, idx)
            logs, err = await resp.next()
        else:
            break
        idx += 1


async def get_logs(
    client: Client,
    max_results: int | None = None,
    since: datetime.datetime | None = None,
) -> list[LogEvent]:
    logs = []
    async for log in iter_logs(client, max_results=max_results, since=since):
        logs.append(log)
    return logs


if __name__ == "__main__":
    from ext_okta.auth import create_okta_client

    since = datetime.datetime.now() - datetime.timedelta(seconds=30)

    async def main():
        client = create_okta_client()
        logs = await get_logs(client, since=since)
        for log in logs:
            print(json.dumps(log.as_dict(), indent=2))

    asyncio.run(main())
