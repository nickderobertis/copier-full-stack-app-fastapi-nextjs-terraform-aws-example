from playwright.sync_api import Page
from tests.fixtures.url import fe
from tests.fixtures.user_details import UserDetails
from tests.nav.login import go_to_log_in_from_nav_bar


def go_to_forgot_password_from_login(page: Page):
    page.locator("text=Forgot password?").click()
    page.wait_for_url(fe("forgot-password"))


def go_to_forgot_password_from_nav_bar(page: Page):
    go_to_log_in_from_nav_bar(page)
    go_to_forgot_password_from_login(page)


def fill_forgot_password(page: Page, user_details: UserDetails):
    email = page.locator('[placeholder="Email address"]')
    email.fill(user_details.email)
    email.press("Enter")
    page.wait_for_url(fe(f"forgot-password-submitted?email={user_details.email}"))
