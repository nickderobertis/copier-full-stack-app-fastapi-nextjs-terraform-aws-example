import pytest
from pydantic import BaseModel
from tests.fixtures.email import *


class GoogleUserDetails(BaseModel):
    email: str
    password: str


@pytest.fixture
def google_user_details() -> GoogleUserDetails:
    # Generate a random email address
    yield GoogleUserDetails(
        email=SETTINGS.google_user,
        password=SETTINGS.google_password,
    )
