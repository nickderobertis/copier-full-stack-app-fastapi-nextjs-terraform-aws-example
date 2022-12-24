from typing import TYPE_CHECKING

from ext_google.auth import login_get_credentials
from ext_google.reports.query.tokens import query_token_authorization
from ext_google.reports.service import create_reports_service

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity


def get_google_token_events(max_results: int | None = None) -> list["Activity"]:
    creds = login_get_credentials()
    service = create_reports_service(creds)
    return list(query_token_authorization(service, max_results=max_results))


if __name__ == "__main__":
    max_res = 5
    print(get_google_token_events(max_results=max_res))
