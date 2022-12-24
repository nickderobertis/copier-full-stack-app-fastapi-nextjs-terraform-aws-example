from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.url import fe
from tests.fixtures.user import UserDetails, user_details
from tests.nav.account.delete import delete_account
from tests.nav.account.nav import go_to_account_page_from_nav_bar
from tests.nav.navbar.profile_dropdown import get_profile_dropdown
from tests.nav.signup import go_to_sign_up_from_nav_bar, sign_up_with_keyboard


def test_delete_account_success_leads_to_sign_up(page: Page, user_details: UserDetails):
    page.goto(fe())
    go_to_sign_up_from_nav_bar(page)
    sign_up_with_keyboard(page, user_details)
    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()

    # Clean up user
    go_to_account_page_from_nav_bar(page)
    delete_account(page, user_details)

    page.locator("#delete-account-success >> button").click()
    page.wait_for_url(fe("signup"))
