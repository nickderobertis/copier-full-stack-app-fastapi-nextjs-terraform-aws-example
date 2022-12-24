import pytest
from playwright.sync_api import Page
from pydantic import BaseModel
from tests.fixtures.google_user_details import GoogleUserDetails
from tests.fixtures.url import fe
from tests.fixtures.user_details import *
from tests.nav.account.delete import delete_account, delete_social_only_account
from tests.nav.account.nav import go_to_account_page_from_nav_bar
from tests.nav.login import go_to_log_in_from_nav_bar, log_in_with_keyboard
from tests.nav.logout import get_logout_redirect_path
from tests.nav.navbar.profile_dropdown import get_profile_dropdown, is_logged_in
from tests.nav.signup import go_to_sign_up_from_nav_bar, sign_up_with_keyboard


def _sign_up(page: Page, user_details: UserDetails):
    page.goto(fe())
    go_to_sign_up_from_nav_bar(page)
    sign_up_with_keyboard(page, user_details)
    profile_dropdown = get_profile_dropdown(page)
    profile_dropdown.wait_for()


def _delete_account(page: Page, user_details: UserDetails):
    if not is_logged_in(page):
        path = get_logout_redirect_path(page.url)
        go_to_log_in_from_nav_bar(page)
        log_in_with_keyboard(page, user_details, expected_path=path)

    go_to_account_page_from_nav_bar(page)
    delete_account(page, user_details)


@pytest.fixture
def user(page: Page, user_details: UserDetails):
    _sign_up(page, user_details)
    yield
    _delete_account(page, user_details)


@pytest.fixture
def user_real_email(page: Page, user_details_real_email: UserDetails):
    user_details = user_details_real_email

    _sign_up(page, user_details)
    yield
    _delete_account(page, user_details)
