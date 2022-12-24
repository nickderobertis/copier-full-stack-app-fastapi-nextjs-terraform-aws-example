from playwright.sync_api import Page, expect
from tests.fixtures.email import *
from tests.fixtures.user import *
from tests.nav.account.update_details import (
    get_current_email_display,
    get_current_name_display,
    update_account_details,
)
from tests.nav.logout import log_out_from_nav_bar


def test_update_name_and_email(page: Page, user, user_details: UserDetails):
    go_to_account_page_from_nav_bar(page)
    new_first_name = "Mary"
    new_last_name = "Doe"
    new_name = f"{new_first_name} {new_last_name}"
    new_email = "test2@test.com"
    new_details = update_account_details(
        page, user_details, new_first_name, new_last_name, new_email
    )
    assert new_details.first_name == new_first_name
    assert new_details.last_name == new_last_name
    assert new_details.email == new_email

    expect(get_current_name_display(page)).to_contain_text(new_name)
    expect(get_current_email_display(page)).to_contain_text(new_email)

    log_out_from_nav_bar(page)
    go_to_log_in_from_nav_bar(page)
    log_in_with_keyboard(page, new_details)

    profile_dropdown = get_profile_dropdown(page)
    expect(profile_dropdown).to_be_visible()

    # Change email back so user can be cleaned up properly
    go_to_account_page_from_nav_bar(page)
    update_account_details(page, new_details, email=user_details.email)
