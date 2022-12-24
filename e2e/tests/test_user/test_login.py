from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.google_user_details import *
from tests.fixtures.user import *
from tests.nav.logout import log_out_from_nav_bar


def test_login(page: Page, user, user_details: UserDetails):
    log_out_from_nav_bar(page)
    go_to_log_in_from_nav_bar(page)
    log_in_with_keyboard(page, user_details)

    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()
