from __future__ import annotations

import json
from typing import TYPE_CHECKING, Iterator

from ext_google.ext_request import log_request
from ext_google.settings import GOOGLE_SETTINGS

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.resources import ReportsResource
    from googleapiclient._apis.admin.reports_v1.schemas import Activity


def query_token_authorization(
    service: ReportsResource,
    max_results: int | None = None,
    num_retries: int = GOOGLE_SETTINGS.default_retries,
) -> Iterator["Activity"]:
    # Call the Admin SDK Reports API
    if max_results is not None:
        # Execute single request to get that many records
        request = service.activities().list(
            userKey="all", applicationName="token", maxResults=max_results
        )
        log_request(request)
        results = request.execute(num_retries=num_retries)
        yield from results.get("items", [])
        return

    # Execute multiple requests to get all records
    request = service.activities().list(userKey="all", applicationName="token")
    idx = 1
    while request is not None:
        log_request(request, index=idx)
        results = request.execute(num_retries=num_retries)
        items = results.get("items", [])
        yield from items
        request = service.activities().list_next(
            previous_request=request, previous_response=results
        )
        idx += 1


if __name__ == "__main__":
    from ext_google.auth import login_get_credentials
    from ext_google.reports.service import create_reports_service

    max_res = 5

    creds = login_get_credentials()
    service = create_reports_service(creds)
    activities = list(query_token_authorization(service, max_results=max_res))

    if not activities:
        print("No logins found.")
    else:
        print(json.dumps(activities, indent=2))
