"""
Get event JSON from Sentry.
"""
import requests
from exc import APIError
from ext_sentry.models.generated.list_event import SentryListEventResponse
from logger import log
from requests import Response
from settings import SETTINGS, Settings


def _get_event_data_page_response(
    url: str, full: bool = False, settings: Settings = SETTINGS
) -> Response:
    if not settings.sentry_auth_token:
        raise ValueError("Sentry API token not set")
    log.info(f"Requesting {url}")
    resp = requests.get(
        url,
        headers={"Authorization": f"Bearer {settings.sentry_auth_token}"},
        params=dict(full=full),
    )
    if not resp.status_code == 200:
        raise APIError("Failed to get event JSON from Sentry", resp)
    return resp


def _get_event_data(
    organization_slug: str,
    project_slug: str,
    full: bool = False,
    page_limit: int = 1,
    settings: Settings = SETTINGS,
) -> list[dict]:
    """
    Get event JSON from Sentry.

    Args:
        full: Whether to get the full event data or just overview details.
        page_limit: The maximum number of pages to get. Set to 0 to get all pages.

    Returns:
        The event JSON.
    """
    url = f"https://sentry.io/api/0/projects/{organization_slug}/{project_slug}/events/"
    current_page = 1
    all_event_data: list[dict] = []
    while current_page <= page_limit or page_limit == 0:
        resp = _get_event_data_page_response(url, full=full, settings=settings)
        events = resp.json()
        if not events:
            break
        all_event_data.extend(events)
        if resp.links["next"]["results"] == "false":
            break
        current_page += 1
        url = resp.links["next"]["url"]

    return all_event_data


def get_event_data(
    organization_slug: str,
    project_slug: str,
    full: bool = False,
    page_limit: int = 1,
    settings: Settings = SETTINGS,
) -> SentryListEventResponse:
    """
    Get event data from Sentry.

    Args:
        full: Whether to get the full event data or just overview details.
        page_limit: The maximum number of pages to get. Set to 0 to get all pages.

    Returns:
        The event response as a pydantic model.
    """
    return SentryListEventResponse(
        __root__=_get_event_data(  # type: ignore
            organization_slug,
            project_slug,
            full=full,
            page_limit=page_limit,
            settings=settings,
        )
    )


if __name__ == "__main__":
    data = get_event_data(
        SETTINGS.sentry_organization_slug, SETTINGS.sentry_fe_project_slug, full=True
    )
    print(data.json(indent=2))
