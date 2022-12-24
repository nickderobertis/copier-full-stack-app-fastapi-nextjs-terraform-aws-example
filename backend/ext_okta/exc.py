from okta.errors.http_error import HTTPError


class OktaException(Exception):
    pass


class OktaHTTPException(OktaException):
    def __init__(self, http_error: HTTPError):
        self.http_error = http_error
        self.message = http_error.message
        self.status_code = http_error.status
        self.url = http_error.url
        full_message = f"Failed to request {self.url} with status {self.status_code}. Reason: {self.message}"
        super().__init__(full_message)
