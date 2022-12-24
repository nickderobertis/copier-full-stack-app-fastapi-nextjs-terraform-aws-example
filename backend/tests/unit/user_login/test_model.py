from pathlib import Path
from typing import TYPE_CHECKING

from okta.models import LogEvent
from tests.fixtures.okta_log_events import okta_log_events
from tests.fixtures.temp_dir import temp_dir
from tests.fixtures.user_login_events import *
from user_login.model import EventSource, UserLoginEvents

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity

from tests.fixtures.google_activity import (
    google_login_activities,
    google_token_activities,
)


def test_create_user_login_models_from_google_login_activity(
    google_login_activities: list["Activity"],
):
    events = UserLoginEvents.from_google_login_activities(google_login_activities)
    assert len(events) == 5
    for event in events:
        assert event.source == EventSource.GOOGLE
        assert event.target_name == "Google Login"
        assert event.target_id == "Google Login"


def test_create_user_login_models_from_google_token_activity(
    google_token_activities: list["Activity"],
):
    events = UserLoginEvents.from_google_token_activities(google_token_activities)
    assert len(events) == 5
    for event in events:
        assert event.source == EventSource.GOOGLE
        # Should be custom app info
        assert event.target_name != "Google Login"
        assert event.target_id != "Google Login"


def test_create_user_login_models_from_okta_log_event(
    okta_log_events: list[LogEvent],
):
    events = UserLoginEvents.from_okta_log_events(okta_log_events)
    assert len(events) == 5
    for event in events:
        assert event.source == EventSource.OKTA


def test_events_to_df(user_login_events: UserLoginEvents):
    df = user_login_events.to_df()
    assert len(df) == 15
    assert df.columns.tolist() == [
        "time",
        "user_id",
        "user_email",
        "target_name",
        "target_id",
        "source",
    ]


def test_events_to_csv(user_login_events: UserLoginEvents, temp_dir: Path):
    csv_path = temp_dir / "user_login_events.csv"
    user_login_events.to_csv(csv_path)
    assert csv_path.exists()
    # 15 data lines and one header line
    assert len(csv_path.read_text().splitlines()) == 16
