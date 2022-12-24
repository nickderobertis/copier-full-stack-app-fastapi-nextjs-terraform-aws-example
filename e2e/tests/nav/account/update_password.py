from playwright.sync_api import Page
from tests.fixtures.user_details import UserDetails


def update_password(page: Page, user: UserDetails, password: str) -> UserDetails:
    current_password = page.locator('[placeholder="Current Password"]')
    new_password = page.locator('[placeholder="New Password"]')
    current_password.click()
    current_password.fill(user.password)
    new_password.click()
    new_password.fill(password)
    page.locator('button:has-text("Update my Password")').click()
    page.locator('button:has-text("Success")').wait_for()

    new_details = user.copy(update=dict(password=password))
    return new_details
