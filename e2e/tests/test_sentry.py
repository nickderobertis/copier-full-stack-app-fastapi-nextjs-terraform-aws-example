import time
from datetime import datetime, timedelta, timezone

import requests
from ext_sentry.get_events import get_event_data
from ext_sentry.models.event import SentryEvent
from playwright.sync_api import Page, expect
from tests.fixtures.dev import dev_only
from tests.fixtures.email import *
from tests.fixtures.url import fe
from tests.fixtures.user import UserDetails, user_details
from tests.nav.account.delete import delete_account
from tests.nav.account.nav import go_to_account_page_from_nav_bar
from tests.nav.dev import go_to_dev_page
from tests.nav.navbar.profile_dropdown import get_profile_dropdown
from tests.nav.signup import go_to_sign_up_from_nav_bar, sign_up_with_keyboard


def get_fe_sentry_events() -> list[SentryEvent]:
    raw_items = get_event_data(
        organization_slug=SETTINGS.sentry_organization_slug,
        project_slug=SETTINGS.sentry_fe_project_slug,
    ).__root__
    return [SentryEvent.from_response_list_item(item) for item in raw_items]


def get_api_sentry_events() -> list[SentryEvent]:
    raw_items = get_event_data(
        organization_slug=SETTINGS.sentry_organization_slug,
        project_slug=SETTINGS.sentry_api_project_slug,
    ).__root__
    return [SentryEvent.from_response_list_item(item) for item in raw_items]


@dev_only
def test_sentry_logging_from_fe(page: Page):
    go_to_dev_page(page)

    # Click the buttons to trigger Sentry events
    page.click("text=Unexpected Exception")
    page.click("text=Caught Exception")
    page.click("text=Log info message to Sentry")
    page.click("text=Log warning message to Sentry")
    page.click("text=Log error message to Sentry")

    # Wait for Sentry events to be populated
    time.sleep(15)

    sentry_events = get_fe_sentry_events()
    recent_events: list[SentryEvent] = []
    for event in sentry_events:
        fifteen_seconds_ago = datetime.now(timezone.utc) - timedelta(seconds=25)
        if event.created > fifteen_seconds_ago:
            recent_events.append(event)

    found_unexpected_exception = False
    found_caught_exception = False
    found_info_message = False
    found_warning_message = False
    found_error_message = False
    for event in recent_events:
        if event.title == "Error: Test unexpected error":
            found_unexpected_exception = True
        if event.title == "Error: Test caught error":
            found_caught_exception = True
        if event.title == "app: Test captured message info level":
            found_info_message = True
        if event.title == "app: Test captured message warning level":
            found_warning_message = True
        if event.title == "app: Test captured message error level":
            found_error_message = True

    assert found_unexpected_exception
    assert found_caught_exception
    assert found_info_message
    assert found_warning_message
    assert found_error_message


@dev_only
def test_sentry_logging_from_api():
    error_url = f"{SETTINGS.api_url}/dev/error"
    response = requests.get(error_url)
    assert response.status_code == 500

    # Wait for Sentry events to be populated
    time.sleep(15)

    sentry_events = get_api_sentry_events()
    recent_events: list[SentryEvent] = []
    for event in sentry_events:
        fifteen_seconds_ago = datetime.now(timezone.utc) - timedelta(seconds=25)
        if event.created > fifteen_seconds_ago:
            recent_events.append(event)

    found_unexpected_exception = False

    for event in recent_events:
        if event.title == "Exception: This is a test error":
            found_unexpected_exception = True

    assert found_unexpected_exception
