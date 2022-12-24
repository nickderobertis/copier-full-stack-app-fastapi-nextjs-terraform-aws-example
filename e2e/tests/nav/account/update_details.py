from playwright.sync_api import Locator, Page
from tests.fixtures.user_details import UserDetails


def get_update_details_form(page: Page) -> Locator:
    return page.locator("#update-account-details")


def get_current_name_display(page: Page) -> Locator:
    return page.locator("#current-name")


def get_current_email_display(page: Page) -> Locator:
    return page.locator("#current-email")


def update_account_details(
    page: Page,
    user: UserDetails,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
) -> UserDetails:
    details_form = get_update_details_form(page)
    name_field = details_form.locator('[placeholder="Name"]')
    email_field = details_form.locator('[placeholder="Email address"]')
    password_field = details_form.locator('[placeholder="Password"]')
    if first_name is not None and last_name is None:
        raise ValueError("must supply both names together")
    if last_name is not None and first_name is None:
        raise ValueError("must supply both names together")
    if first_name is not None and last_name is not None:
        name = f"{first_name} {last_name}"
        name_field.click()
        name_field.fill(name)
    if email is not None:
        email_field.click()
        email_field.fill(email)
    password_field.click()
    password_field.fill(user.password)
    page.locator('button:has-text("Update my Account")').click()
    page.locator('button:has-text("Success")').wait_for()

    new_details = user.copy(
        update=dict(
            first_name=first_name or user.first_name,
            last_name=last_name or user.last_name,
            email=email or user.email,
        )
    )
    return new_details
