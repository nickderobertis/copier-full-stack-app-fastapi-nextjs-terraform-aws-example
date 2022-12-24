from logger import log
from okta.api_response import OktaAPIResponse


def response_to_info_log_str(resp: OktaAPIResponse, index: int | None = None) -> str:
    return f"Request {index} to {resp._url} had status {resp.get_status()}"


def response_to_debug_log_str(resp: OktaAPIResponse) -> str:
    return f"Response had Body: {resp.get_body()}\nHeaders: {resp.get_headers()}"


def log_response(resp: OktaAPIResponse, index: int | None = None) -> None:
    log.info(response_to_info_log_str(resp, index=index))
    log.debug(response_to_debug_log_str(resp))


def log_next_request(resp: OktaAPIResponse, index: int | None = None) -> None:
    log.info(f"Sending request {index} for next url: {resp._next}")
