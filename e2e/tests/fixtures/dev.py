import functools

import pytest
from settings import SETTINGS


def dev_only(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not SETTINGS.enable_dev_only_tests:
            pytest.skip("Skipping test in production environment")
        return func(*args, **kwargs)

    return wrapper
