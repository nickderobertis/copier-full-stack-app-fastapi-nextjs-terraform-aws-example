import asyncio
import datetime
from pathlib import Path

from batch_download.config import OKTA_CONVERTED_FOLDER
from batch_download.date_file import get_dated_file_name
from ext_okta.auth import create_okta_client
from ext_okta.get_logs import iter_logs
from ext_okta.settings import OKTA_SETTINGS, OktaSettings
from logger import log
from okta.models import LogEvent
from user_login.model import UserLoginEvents


async def batch_download_all_okta_history_to_parquet(
    out_dir: Path = OKTA_CONVERTED_FOLDER,
    settings: OktaSettings = OKTA_SETTINGS,
    since: datetime.datetime | None = None,
    buffer_size: int = 100000,
) -> None:
    client = create_okta_client(settings)
    since = since or datetime.datetime.now() - datetime.timedelta(days=180)
    log_buffer: list[LogEvent] = []

    def write_buffer():
        # Name file based on the timestamp from the activity
        events = UserLoginEvents.from_okta_log_events(log_buffer)
        last_event = events[-1]
        out_file = out_dir / get_dated_file_name(last_event.time, extension="parquet")
        log.info(f"Writing {buffer_size} results to {out_file}")
        events.to_parquet(out_file)

    async for event in iter_logs(client, since=since):
        log_buffer.append(event)
        # Every 100,000 records, write to file
        if len(log_buffer) >= buffer_size:
            write_buffer()
            log_buffer = []

    if len(log_buffer) > 0:
        write_buffer()


if __name__ == "__main__":
    asyncio.run(batch_download_all_okta_history_to_parquet())
