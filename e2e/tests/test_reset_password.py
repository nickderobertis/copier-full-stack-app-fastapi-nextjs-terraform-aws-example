import re

from playwright.sync_api import Page, expect
from tempmail3 import wait_for_emails
from tests.fixtures.email import *
from tests.fixtures.user import *
from tests.fixtures.user_details import *
from tests.nav.account.update_password import update_password
from tests.nav.forgot import fill_forgot_password, go_to_forgot_password_from_nav_bar
from tests.nav.logout import log_out_from_nav_bar
from tests.nav.reset import fill_reset_password


def test_reset_password(
    page: Page,
    user_real_email,
    user_details_real_email: UserDetails,
    temp_mail: TempMail,
):
    user_details = user_details_real_email

    log_out_from_nav_bar(page)
    go_to_forgot_password_from_nav_bar(page)
    fill_forgot_password(page, user_details)

    emails = wait_for_emails(temp_mail)
    assert emails is not None
    assert len(emails) == 1
    email = emails[0]
    # Extract the link from the email using a regex to parse <a href="...">...</a>
    link = re.search(r"<a href=\"(.*?)\">", email.mail_text_only).group(1)

    page.goto(link)

    new_password = "bbbbbbbb"
    new_details = fill_reset_password(page, user_details, new_password)
    page.locator('button:has-text("Sign In")').click()
    log_in_with_keyboard(page, new_details)

    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()

    # Change it back so user can be cleaned up properly
    go_to_account_page_from_nav_bar(page)
    update_password(page, new_details, user_details.password)
