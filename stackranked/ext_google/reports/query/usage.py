from __future__ import annotations

import datetime
import json
from typing import TYPE_CHECKING

from ext_google.dates import to_google_api_date_string

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.resources import ReportsResource


def query_user_usage(service: ReportsResource, date: datetime.date):
    """
    NOTE: Needs "https://www.googleapis.com/auth/admin.reports.audit.readonly" scope, which is not
    currently included in SCOPES
    """
    # Call the Admin SDK Reports API
    results = (
        service.userUsageReport()
        .get(userKey="all", date=to_google_api_date_string(date))
        .execute()
    )
    usage = results.get("usageReports", [])

    if not usage:
        print("No usage found.")
    else:
        print("Usage:")
        print(json.dumps(usage, indent=2))


if __name__ == "__main__":
    from ext_google.auth import login_get_credentials
    from ext_google.reports.service import create_reports_service

    py_date = datetime.date(2022, 8, 2)

    creds = login_get_credentials()
    service = create_reports_service(creds)
    query_user_usage(service, py_date)
