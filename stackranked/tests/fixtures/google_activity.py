import json
from typing import TYPE_CHECKING

import pytest
from tests.config import GOOGLE_LOGIN_RESPONSE_PATH, GOOGLE_TOKEN_RESPONSE_PATH

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity


@pytest.fixture
def google_login_activities() -> list["Activity"]:
    return json.loads(GOOGLE_LOGIN_RESPONSE_PATH.read_text())


@pytest.fixture
def google_token_activities() -> list["Activity"]:
    return json.loads(GOOGLE_TOKEN_RESPONSE_PATH.read_text())
