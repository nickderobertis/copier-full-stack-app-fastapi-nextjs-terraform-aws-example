from playwright.sync_api import Page
from tests.fixtures.google_user_details import GoogleUserDetails
from tests.fixtures.url import fe
from tests.fixtures.user import UserDetails

DELETE_ACCOUNT_SELECTOR = "#delete-account"


def in_delete_account_selector(selector: str) -> str:
    return f"{DELETE_ACCOUNT_SELECTOR} >> {selector}"


def delete_account(page: Page, user: UserDetails):
    s = in_delete_account_selector

    email = page.locator(s('[placeholder="Email address"]'))
    password = page.locator(s('[placeholder="Password"]'))
    email.click()
    email.fill(user.email)
    email.click()
    email.press("Tab")
    password.fill(user.password)
    password.press("Enter")
    page.wait_for_url(fe("delete-account-success"))


def delete_social_only_account(page: Page, user: GoogleUserDetails):
    s = in_delete_account_selector

    email = page.locator(s('[placeholder="Email address"]'))
    email.click()
    email.fill(user.email)
    email.click()
    email.press("Enter")
    page.wait_for_url(fe("delete-account-success"))
