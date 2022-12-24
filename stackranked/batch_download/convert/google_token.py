import json
from pathlib import Path

from batch_download.config import GOOGLE_CONVERTED_FOLDER, GOOGLE_DATA_FOLDER
from logger import log
from rich.progress import track
from user_login.model import UserLoginEvents


def _convert_json_google_token_file_to_parquet(in_path: Path, out_path: Path):
    data = json.loads(in_path.read_text())
    events = UserLoginEvents.from_google_token_activities(data)
    events.to_parquet(out_path)


def convert_all_json_google_token_files_to_parquet(
    in_path: Path = GOOGLE_DATA_FOLDER, out_path: Path = GOOGLE_CONVERTED_FOLDER
):
    files = list(in_path.glob("*.json"))
    log.info(f"Converting {len(files)} files")
    for in_file in track(files, description="Converting Google Token Files"):
        out_file = (out_path / in_file.name).with_suffix(".parquet")
        log.info(f"Converting {in_file} to {out_file}")
        _convert_json_google_token_file_to_parquet(in_file, out_file)


if __name__ == "__main__":
    convert_all_json_google_token_files_to_parquet()
