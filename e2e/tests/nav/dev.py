from playwright.sync_api import Page
from tests.fixtures.url import fe


def go_to_dev_page(page: Page):
    page.goto(fe("dev"))
