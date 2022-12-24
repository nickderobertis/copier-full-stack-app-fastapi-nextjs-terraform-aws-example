from playwright.sync_api import Page
from settings import SETTINGS
from tests.fixtures import url


def navigate_to_login_and_login(page: Page):
    page.goto(url.monitoring("login"))
    page.locator('[placeholder="email or username"]').click()
    page.locator('[placeholder="email or username"]').fill("admin")
    page.locator('[placeholder="email or username"]').press("Tab")
    page.locator('[placeholder="password"]').fill(SETTINGS.grafana_password)
    page.locator('[placeholder="password"]').press("Enter")
    page.wait_for_url(url.monitoring("?orgId=1"))
