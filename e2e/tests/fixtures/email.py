import pytest
from settings import SETTINGS
from tempmail3 import TempMail


@pytest.fixture(scope="session")
def temp_mail() -> TempMail:
    yield TempMail(SETTINGS.rapid_api_key)


@pytest.fixture(scope="session")
def email(temp_mail: TempMail) -> str:
    yield temp_mail.get_email_address()


if __name__ == "__main__":
    tm = TempMail(
        SETTINGS.rapid_api_key, api_domain="privatix-temp-mail-v1.p.rapidapi.com"
    )
    print(tm.get_email_address())
    print(tm.get_mailbox())
