from googleapiclient.http import HttpRequest
from logger import log


def request_to_log_info_str(request: HttpRequest, index: int | None = None) -> str:
    index_str = f" {index}" if index is not None else ""
    return f"Executing request{index_str}: {request.method} {request.uri}"


def request_to_log_debug_str(request: HttpRequest) -> str:
    return f"Request has Body: {request.body}\nHeaders: {request.headers}"


def log_request(request: HttpRequest, index: int | None = None) -> None:
    log.info(request_to_log_info_str(request, index=index))
    log.debug(request_to_log_debug_str(request))
