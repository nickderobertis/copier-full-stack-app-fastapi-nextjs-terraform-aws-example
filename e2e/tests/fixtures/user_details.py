import random
import string

import pytest
from pydantic import BaseModel
from tests.fixtures.email import *

VALID_PASSWORD = "aaaaaaaa"


class UserDetails(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}"


def random_char(char_num):
    return "".join(random.choice(string.ascii_letters) for _ in range(char_num))


@pytest.fixture
def user_details() -> UserDetails:
    # Generate a random email address
    email = f"test+{random_char(5)}@example.com"
    yield UserDetails(
        first_name="Joe",
        last_name="Smith",
        email=email,
        password=VALID_PASSWORD,
    )


@pytest.fixture
def user_details_real_email(email: str) -> UserDetails:
    yield UserDetails(
        first_name="Mary",
        last_name="Jones",
        email=email,
        password=VALID_PASSWORD,
    )
