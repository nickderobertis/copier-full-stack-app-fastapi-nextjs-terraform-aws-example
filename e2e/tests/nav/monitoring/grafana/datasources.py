from playwright.sync_api import Page, expect
from tests.fixtures import url


def navigate_to_prometheus_data_source_and_test(page: Page):
    navigate_to_prometheus_data_source(page)
    save_and_test(page)


def navigate_to_cloudwatch_data_source_and_test(page: Page):
    navigate_to_cloudwatch_data_source(page)
    save_and_test(page)


def navigate_to_data_sources(page: Page):
    page.locator('[aria-label="Configuration"]').hover()
    page.locator("text=Data sources").click()
    page.wait_for_url(url.monitoring("datasources"))


def navigate_to_prometheus_data_source(page: Page):
    navigate_to_data_sources(page)
    page.locator('h2:has-text("Prometheus")').click()


def navigate_to_cloudwatch_data_source(page: Page):
    navigate_to_data_sources(page)
    page.locator('h2:has-text("CloudWatch")').click()


def save_and_test(page: Page):
    page.locator(
        '[aria-label="Data source settings page Save and Test button"]'
    ).click()
    # Find the alert and ensure it says "Data source is working"
    expect(page.locator("text=Data source is working")).to_be_visible()
