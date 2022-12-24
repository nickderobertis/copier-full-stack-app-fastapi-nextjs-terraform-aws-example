from pathlib import Path

import dask.dataframe as dd
from dask import dataframe as dd
from user_login.analysis.config import EMAIL_COL, SOURCE_COL, TARGET_NAME_COL
from user_login.analysis.from_df import output_analysis_df_dict_to_csv


def user_app_usage_from_event_df(df: dd.DataFrame) -> dd.DataFrame:
    return (
        df.groupby([TARGET_NAME_COL, EMAIL_COL])
        .count()
        .sort_values(by=[TARGET_NAME_COL, EMAIL_COL])[SOURCE_COL]
        .to_frame()
    )


def app_usage_from_event_df(df: dd.DataFrame) -> dd.DataFrame:
    return (
        df.groupby([TARGET_NAME_COL])
        .count()
        .sort_values(by=SOURCE_COL, ascending=False)[SOURCE_COL]
        .to_frame()
    )


def user_count_per_app_from_event_df(df: dd.DataFrame) -> dd.DataFrame:
    unique_user_apps = df[[EMAIL_COL, TARGET_NAME_COL]].drop_duplicates()
    return (
        unique_user_apps.groupby([TARGET_NAME_COL])
        .count()
        .sort_values(by=EMAIL_COL, ascending=False)
    )


def analysis_df_dict_from_df(
    df: dd.DataFrame,
) -> dict[str, dd.DataFrame]:
    graph_dict = {
        "user_app_usage": user_app_usage_from_event_df(df),
        "app_usage": app_usage_from_event_df(df),
        "user_count_per_app": user_count_per_app_from_event_df(df),
    }
    return {name: df.compute() for name, df in graph_dict.items()}


def create_and_output_analysis_dict(df: dd.DataFrame, out_path: Path):
    analysis_dict = analysis_df_dict_from_df(df)
    output_analysis_df_dict_to_csv(analysis_dict, out_path)
