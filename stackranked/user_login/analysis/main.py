from pathlib import Path

from ext_google.reports.tokens import get_google_token_events
from ext_okta.main import get_user_login_events
from ext_okta.settings import OKTA_SETTINGS, OktaSettings
from user_login.analysis.from_df import (
    analysis_df_dict_from_user_events,
    output_analysis_df_dict_to_csv,
)
from user_login.model import UserLoginEvents


def main_user_login_analysis(
    okta_settings: OktaSettings = OKTA_SETTINGS,
    out_dir: Path | None = None,
    max_results: int | None = None,
):
    if out_dir is None:
        out_dir = Path.cwd()
    out_dir.mkdir(exist_ok=True, parents=True)

    okta_logs = get_user_login_events(max_results=max_results, settings=okta_settings)
    okta_events = UserLoginEvents.from_okta_log_events(okta_logs)

    google_logs = get_google_token_events(max_results=max_results)
    google_events = UserLoginEvents.from_google_token_activities(google_logs)
    all_events = okta_events.merge(google_events)

    okta_analysis_dict = analysis_df_dict_from_user_events(okta_events)
    okta_path = out_dir / "Okta"
    okta_path.mkdir(exist_ok=True, parents=True)
    output_analysis_df_dict_to_csv(okta_analysis_dict, okta_path)

    google_analysis_dict = analysis_df_dict_from_user_events(google_events)
    google_path = out_dir / "Google"
    google_path.mkdir(exist_ok=True, parents=True)
    output_analysis_df_dict_to_csv(google_analysis_dict, google_path)

    all_analysis_dict = analysis_df_dict_from_user_events(all_events)
    all_path = out_dir / "All"
    all_path.mkdir(exist_ok=True, parents=True)
    output_analysis_df_dict_to_csv(all_analysis_dict, all_path)


if __name__ == "__main__":
    main_user_login_analysis()
