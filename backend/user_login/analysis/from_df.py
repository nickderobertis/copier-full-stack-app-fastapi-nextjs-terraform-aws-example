import asyncio
from pathlib import Path

import pandas as pd
from ext_okta.auth import create_okta_client
from ext_okta.get_logs import get_logs
from user_login.analysis.config import EMAIL_COL, SOURCE_COL, TARGET_NAME_COL
from user_login.model import UserLoginEvents


def user_app_usage_from_event_df(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        df.groupby([TARGET_NAME_COL, EMAIL_COL])[SOURCE_COL].count()
    ).sort_values(by=[TARGET_NAME_COL, EMAIL_COL])


def app_usage_from_event_df(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        df.groupby([TARGET_NAME_COL])[SOURCE_COL].count().sort_values(ascending=False)
    )


def user_count_per_app_from_event_df(df: pd.DataFrame) -> pd.DataFrame:
    unique_user_apps = df[[EMAIL_COL, TARGET_NAME_COL]].drop_duplicates()
    return (
        unique_user_apps.groupby([TARGET_NAME_COL])
        .count()
        .sort_values(by=EMAIL_COL, ascending=False)
    )


def analysis_df_dict_from_user_events(
    events: UserLoginEvents,
) -> dict[str, pd.DataFrame]:
    df = events.to_df()
    return analysis_df_dict_from_df(df)


def analysis_df_dict_from_df(
    df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    return {
        "user_app_usage": user_app_usage_from_event_df(df),
        "app_usage": app_usage_from_event_df(df),
        "user_count_per_app": user_count_per_app_from_event_df(df),
        "all_events": df,
    }


def output_analysis_df_dict_to_csv(
    analysis_df_dict: dict[str, pd.DataFrame], output_dir: Path
):
    for name, df in analysis_df_dict.items():
        df.to_csv(output_dir / f"{name}.csv")


def output_analysis_for_user_events(events: UserLoginEvents, output_dir: Path):
    analysis_dict = analysis_df_dict_from_user_events(events)
    output_analysis_df_dict_to_csv(analysis_dict, output_dir)


if __name__ == "__main__":
    from ext_google.auth import login_get_credentials
    from ext_google.reports.query.tokens import query_token_authorization
    from ext_google.reports.service import create_reports_service

    max_res = 5

    creds = login_get_credentials()
    service = create_reports_service(creds)
    google_activities = list(query_token_authorization(service, max_results=max_res))
    google_events = UserLoginEvents.from_google_token_activities(google_activities)

    client = create_okta_client()
    logs = asyncio.run(get_logs(client, max_results=max_res))
    okta_events = UserLoginEvents.from_okta_log_events(logs)

    all_events = google_events.merge(okta_events)
    output_analysis_for_user_events(all_events, Path.cwd())
