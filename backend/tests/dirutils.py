import contextlib
import os
import shutil
import tempfile
from pathlib import Path
from typing import Iterator


def create_temp_path() -> Path:
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir).resolve()
    return temp_path


@contextlib.contextmanager
def temp_path() -> Iterator[Path]:
    """
    Returns a temporary folder path

    Use this instead of tempfile.TemporaryDirectory because:
    1. That returns a string and not a path
    2. On MacOS, the temp directory has a symlink. This resolves the symlink so that
       there won't be any mismatch in resolved paths.
    3. On Windows, the temp directory can fail to delete with a PermissionError. This function
       will try to delete the temp directory, but if it fails with an error it will just ignore it.
    """
    temp_path = create_temp_path()
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@contextlib.contextmanager
def change_directory_to(path: Path):
    current_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(current_path)
