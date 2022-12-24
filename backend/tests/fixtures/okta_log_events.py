import json

import pytest
from okta.models import LogEvent
from tests.config import OKTA_LOGIN_RESPONSE_PATH


@pytest.fixture
def okta_log_events() -> list[LogEvent]:
    data = json.loads(OKTA_LOGIN_RESPONSE_PATH.read_text())
    return [LogEvent(event_dict) for event_dict in data]
