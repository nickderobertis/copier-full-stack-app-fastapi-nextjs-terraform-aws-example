from playwright.sync_api import Locator, Page


def get_nav_bar(page: Page) -> Locator:
    return page.locator("#nav-bar")
