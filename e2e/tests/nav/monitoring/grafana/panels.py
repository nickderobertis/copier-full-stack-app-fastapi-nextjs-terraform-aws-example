from playwright.sync_api import Locator, Page


def locate_panel_by_name(page: Page, panel_name: str) -> Locator:
    return page.locator(f'[aria-label="{panel_name} panel"]')
