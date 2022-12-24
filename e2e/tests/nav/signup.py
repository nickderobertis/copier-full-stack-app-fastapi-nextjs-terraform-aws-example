from playwright.sync_api import Page
from tests.fixtures.url import fe
from tests.fixtures.user import UserDetails


def go_to_sign_up_from_nav_bar(page: Page):
    # Click text=Sign up for free
    page.locator("text=Sign up for free").click()
    page.wait_for_url(fe("signup"))


def sign_up_with_keyboard(page: Page, user: UserDetails):
    name = page.locator('div[role="dialog"] [placeholder="Name"]')
    email = page.locator('div[role="dialog"] [placeholder="Email address"]')
    name.click()
    name.fill(user.name)
    name.press("Tab")
    email.fill(user.email)
    email.press("Tab")
    page.locator('div[role="dialog"] [placeholder="Password"]').fill(user.password)
    page.locator('div[role="dialog"] button:has-text("Sign up")').click()
    page.wait_for_url(f"/")
