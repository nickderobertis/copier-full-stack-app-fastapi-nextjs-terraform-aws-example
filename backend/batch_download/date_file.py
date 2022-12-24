import datetime

FILE_DATETIME_FORMAT = "%Y-%m-%d-%H-%M-%S"


def get_dated_file_name(dt: datetime.datetime, extension: str = "json") -> str:
    return dt.strftime(FILE_DATETIME_FORMAT) + f".{extension}"
