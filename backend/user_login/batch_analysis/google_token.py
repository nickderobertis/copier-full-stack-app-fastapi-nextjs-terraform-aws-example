from datetime import datetime, timedelta
from pathlib import Path

import dask.dataframe as dd
import pandas as pd
from batch_download.config import GOOGLE_CONVERTED_FOLDER
from logger import log
from user_login.analysis.from_dask import create_and_output_analysis_dict
from user_login.config import GOOGLE_ANALYSIS_DIR


def _df_of_days_into_past(df: dd.DataFrame, days: int) -> dd.DataFrame:
    time_ago = datetime.now() - timedelta(days=days)
    return df[df.time > pd.to_datetime(time_ago).tz_localize("UTC")]


def _output_analysis_of_days_into_past(
    df: dd.DataFrame, days: int, root_out_path: Path
):
    days_df = _df_of_days_into_past(df, days)
    out_path = root_out_path / f"{days}_days"
    out_path.mkdir(exist_ok=True)
    create_and_output_analysis_dict(days_df, out_path)


def analyze_google_token_data_from_parquet_dir(
    in_path: Path = GOOGLE_CONVERTED_FOLDER, out_path: Path = GOOGLE_ANALYSIS_DIR
):
    df = dd.read_parquet(str(in_path))

    log.info("Running analysis on all days")
    full_history_path = out_path / "Full"
    full_history_path.mkdir(exist_ok=True)
    create_and_output_analysis_dict(df, full_history_path)

    for days in [30, 60, 90]:
        log.info(f"Running analysis on {days} days")
        _output_analysis_of_days_into_past(df, days, out_path)


if __name__ == "__main__":
    from dask.diagnostics import ProgressBar

    ProgressBar().register()

    analyze_google_token_data_from_parquet_dir()
