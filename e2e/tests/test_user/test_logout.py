from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.user import *
from tests.nav.logout import log_out_from_nav_bar


def test_logout(page: Page, user):
    log_out_from_nav_bar(page)

    expect(page.locator('div[id="logout-success"]')).to_be_visible()
    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).not_to_be_visible()
