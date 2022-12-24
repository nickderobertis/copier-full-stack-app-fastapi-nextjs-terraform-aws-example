import datetime

from tzlocal import get_localzone


def datetime_to_utc_iso(dt: datetime.datetime) -> str:
    """
    Attaches the local timezone to the incoming time if it does
    not already have a timezone, then converts to the UTC timezone.
    Finally, outputs the date as an ISO string
    """
    if dt.tzinfo is None:
        local_tz = get_localzone()
        dt.replace(tzinfo=local_tz)
    utc_dt = dt.astimezone(tz=datetime.timezone.utc)
    return utc_dt.isoformat()
