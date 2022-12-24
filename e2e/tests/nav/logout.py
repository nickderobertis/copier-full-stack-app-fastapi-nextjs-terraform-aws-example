import re

from playwright.sync_api import Page
from tests.fixtures.url import fe
from tests.nav.navbar.profile_dropdown import get_profile_dropdown

URL_PATTERN = re.compile(r"(?P<base>https?://[^/]+)(?P<path>/.*)")


def log_out_from_nav_bar(page: Page):
    profile_dropdown = get_profile_dropdown(page)
    profile_dropdown.hover()
    profile_dropdown.locator("text=Log out").click()
    page.wait_for_url(fe("logout"))


def get_logout_redirect_path(url: str) -> str:
    # Parse url into base and path using re
    match = URL_PATTERN.match(url)
    path = match.group("path")
    if path in ["/logout", "/login", "/account"]:
        return ""
    return path
