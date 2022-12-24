from playwright.sync_api import Page
from tests.fixtures.url import fe
from tests.nav.navbar.profile_dropdown import get_profile_dropdown


def go_to_account_page_from_nav_bar(page: Page):
    # Click text=Account
    profile_dropdown = get_profile_dropdown(page)
    profile_dropdown.hover()
    profile_dropdown.locator("text=Account").click()
    page.wait_for_url(fe("account"))
