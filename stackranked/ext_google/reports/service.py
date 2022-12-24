from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.resources import ReportsResource

from ext_google.auth import login_get_credentials
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def create_reports_service(creds: Credentials) -> ReportsResource:
    service = build("admin", "reports_v1", credentials=creds)
    return service


if __name__ == "__main__":
    creds = login_get_credentials()
    create_reports_service(creds)
