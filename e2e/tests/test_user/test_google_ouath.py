from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.google_user_details import *
from tests.fixtures.user import *


def test_login_with_google_reaches_google_screen(
    page: Page, google_user_details: GoogleUserDetails
):
    page.goto(fe())
    go_to_log_in_from_nav_bar(page)
    page.locator('#login-form >> text="Log in with Google"').click()
    page.wait_for_selector("text=Google")


def test_connect_with_google_reaches_google_screen(
    page: Page, user, user_details: UserDetails, google_user_details: GoogleUserDetails
):
    go_to_account_page_from_nav_bar(page)
    page.locator('text="Connect Google"').click()
    page.wait_for_selector("text=Google")
    page.goto(fe())
    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()


def test_callback_page_gets_auth_token_and_logs_user_in(page: Page):
    page.route(
        "**/auth/google/callback?code=myCode&state=myState",
        lambda route, request: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"access_token": "12345"}',
        ),
    )
    page.route(
        "**/users/me",
        lambda route, request: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id":"d1b49aa1-a427-4cf3-9bb2-c5b58f8c8061","email":"abc123@gmail.com","is_active":true,"is_superuser":false,"is_verified":false,"name":"Mary Jones","has_real_password":false}',
        ),
    )
    page.goto(fe("auth/google?state=myState&code=myCode"))

    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()
