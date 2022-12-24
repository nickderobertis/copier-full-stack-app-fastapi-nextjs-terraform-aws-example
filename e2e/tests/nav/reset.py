from playwright.sync_api import Page
from tests.fixtures.url import fe
from tests.fixtures.user_details import UserDetails
from tests.nav.login import go_to_log_in_from_nav_bar


def fill_reset_password(
    page: Page, user_details: UserDetails, new_password: str
) -> UserDetails:
    email = page.locator('[placeholder="New Password"]')
    email.fill(new_password)
    email.press("Enter")
    page.wait_for_url(fe(f"reset-password-finish"))

    new_details = user_details.copy(update=dict(password=new_password))
    return new_details
