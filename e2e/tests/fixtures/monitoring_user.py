import pytest
from playwright.sync_api import Page
from tests.nav.monitoring.grafana.login import navigate_to_login_and_login


@pytest.fixture
def monitoring_user(page: Page):
    navigate_to_login_and_login(page)
    yield
