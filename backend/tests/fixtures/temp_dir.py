from pathlib import Path

import pytest
from tests.dirutils import create_temp_path


@pytest.fixture
def temp_dir() -> Path:  # type: ignore
    with create_temp_path() as temp_path:
        yield temp_path
