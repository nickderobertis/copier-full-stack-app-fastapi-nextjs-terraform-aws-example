from typing import TYPE_CHECKING

import pytest
from okta.models import LogEvent

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity

from tests.fixtures.google_activity import (
    google_login_activities,
    google_token_activities,
)
from tests.fixtures.okta_log_events import okta_log_events
from user_login.model import UserLoginEvents


@pytest.fixture
def google_login_user_login_events(
    google_login_activities: list["Activity"],
) -> UserLoginEvents:
    return UserLoginEvents.from_google_login_activities(google_login_activities)


@pytest.fixture
def google_token_user_login_events(
    google_token_activities: list["Activity"],
) -> UserLoginEvents:
    return UserLoginEvents.from_google_token_activities(google_token_activities)


@pytest.fixture
def okta_user_login_events(okta_log_events: list[LogEvent]) -> UserLoginEvents:
    return UserLoginEvents.from_okta_log_events(okta_log_events)


@pytest.fixture
def user_login_events(
    google_login_user_login_events,
    google_token_user_login_events,
    okta_user_login_events,
) -> UserLoginEvents:
    return UserLoginEvents(
        events=[
            *google_login_user_login_events.events,
            *google_token_user_login_events.events,
            *okta_user_login_events.events,
        ]
    )
