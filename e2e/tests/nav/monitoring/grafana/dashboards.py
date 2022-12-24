from playwright.sync_api import Page, expect


def nav_to_dashboards(page: Page):
    page.locator('[aria-label="Search dashboards"]').hover()
    page.locator("text=Search dashboards").click()


def go_to_dashboard_from_search(page: Page, dashboard_name: str):
    page.locator(
        f'[aria-label="Dashboard search item {dashboard_name}"] div:has-text("{dashboard_name}General")'
    ).nth(1).click()
    expect(page.locator(f'[aria-label="Search dashboard by name"]')).to_contain_text(
        dashboard_name
    )
