from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.user import *
from tests.nav.account.update_password import update_password
from tests.nav.logout import log_out_from_nav_bar


def test_update_password(page: Page, user, user_details: UserDetails):
    go_to_account_page_from_nav_bar(page)
    new_password = "bbbbbbbb"
    new_details = update_password(page, user_details, new_password)
    assert new_details.password == new_password

    log_out_from_nav_bar(page)
    go_to_log_in_from_nav_bar(page)
    log_in_with_keyboard(page, new_details)

    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()

    # Change it back so user can be cleaned up properly
    go_to_account_page_from_nav_bar(page)
    update_password(page, new_details, user_details.password)
