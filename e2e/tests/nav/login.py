from ext_time import random_sleep
from playwright.sync_api import Page
from tests.fixtures.google_user_details import GoogleUserDetails
from tests.fixtures.url import fe
from tests.fixtures.user import UserDetails
from tests.nav.navbar.nav import get_nav_bar


def go_to_log_in_from_nav_bar(page: Page):
    # Click text=Sign up for free
    nav_bar = get_nav_bar(page)
    nav_bar.locator("text=Login").click()
    page.wait_for_url(fe("login"))


def log_in_with_keyboard(
    page: Page, user: UserDetails, expected_path: str | None = "/"
):
    email = page.locator('div[role="dialog"] [placeholder="Email address"]')
    password = page.locator('div[role="dialog"] [placeholder="Password"]')

    email.click()
    email.fill(user.email)
    email.press("Tab")
    password.fill(user.password)
    page.locator('#login-form >> text="Log in"').click()
    if expected_path:
        page.wait_for_url(expected_path)
