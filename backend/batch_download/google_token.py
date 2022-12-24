import json
from pathlib import Path
from typing import TYPE_CHECKING

from batch_download.config import GOOGLE_DATA_FOLDER
from batch_download.date_file import get_dated_file_name
from user_login.model import UserLoginEvent

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity

from ext_google.auth import login_get_credentials
from ext_google.reports.query.tokens import query_token_authorization
from ext_google.reports.service import create_reports_service
from ext_google.settings import GOOGLE_SETTINGS, GoogleSettings


def batch_download_all_google_history_to_json(
    out_dir: Path = GOOGLE_DATA_FOLDER,
    google_settings: GoogleSettings = GOOGLE_SETTINGS,
) -> None:
    creds = login_get_credentials()
    service = create_reports_service(creds)

    log_buffer: list["Activity"] = []
    for activity in query_token_authorization(
        service, num_retries=google_settings.default_retries
    ):
        log_buffer.append(activity)
        # Every 100,000 records, write to file
        if len(log_buffer) >= 100000:
            # Name file based on the timestamp from the activity
            last_event = UserLoginEvent.from_google_token_activity(log_buffer[-1])
            out_file = out_dir / get_dated_file_name(last_event.time)
            out_file.write_text(json.dumps(log_buffer, indent=2))
            log_buffer = []


if __name__ == "__main__":
    batch_download_all_google_history_to_json()
