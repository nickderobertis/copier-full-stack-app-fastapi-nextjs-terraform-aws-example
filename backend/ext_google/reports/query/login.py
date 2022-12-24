from __future__ import annotations

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.resources import ReportsResource
    from googleapiclient._apis.admin.reports_v1.schemas import Activity


def query_login_reports(
    service: ReportsResource, max_results: int | None = None
) -> list[Activity]:
    # Call the Admin SDK Reports API
    results = (
        service.activities()
        .list(userKey="all", applicationName="login", maxResults=max_results)
        .execute()
    )
    return results.get("items", [])


if __name__ == "__main__":
    from ext_google.auth import login_get_credentials
    from ext_google.reports.service import create_reports_service

    max_res = 5

    creds = login_get_credentials()
    service = create_reports_service(creds)
    activities = query_login_reports(service, max_results=max_res)

    if not activities:
        print("No logins found.")
    else:
        print("Logins:")
        print(json.dumps(activities, indent=2))
