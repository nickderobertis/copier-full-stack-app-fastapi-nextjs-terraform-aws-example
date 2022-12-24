from playwright.sync_api import Locator, Page


def get_profile_dropdown(page: Page) -> Locator:
    return page.locator('div[id="profile-dropdown"]')


def is_logged_in(page: Page) -> bool:
    return get_profile_dropdown(page).is_visible()
