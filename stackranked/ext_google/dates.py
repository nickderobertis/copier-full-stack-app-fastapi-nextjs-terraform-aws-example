import datetime


def to_google_api_date_string(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")
