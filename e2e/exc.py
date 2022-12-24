from requests import Response


class APIError(RuntimeError):
    """
    When the API return an error code we did not like

    It will combine the user message with the response status and body to create
    the final message, e.g.:

    Examples:
        >>> resp = req.get("something")
        >>> raise APIError("custom message", resp)
        APIError(custom message: Response had status code 400 and body {"error": "Bad Request"})

    Attributes:
        message: A user-defined error message
        resp: The response object from the API

    """

    def __init__(self, message: str, resp: Response):
        self.user_message = message
        self.resp = resp
        full_message = _full_api_error_message(message, resp)
        super().__init__(full_message)


def _full_api_error_message(user_message: str, resp: Response) -> str:
    return f"{user_message}: Response had status code {resp.status_code} and body {resp.text}"
