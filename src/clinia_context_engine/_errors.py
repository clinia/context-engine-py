from __future__ import annotations

import httpx

from .generated.models import ApiError

__all__ = [
    "APIConnectionError",
    "APIStatusError",
    "APITimeoutError",
    "ContextEngineError",
]


class ContextEngineError(Exception):
    """Base class for every error raised by this client."""


class APIConnectionError(ContextEngineError):
    """The request never produced an HTTP response."""

    def __init__(self, message: str, *, request: httpx.Request) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    def __init__(self, *, request: httpx.Request) -> None:
        super().__init__("Request timed out.", request=request)


class APIStatusError(ContextEngineError):
    """A non-2xx HTTP response.

    `error` carries the server's parsed error envelope when the body is a valid
    `ApiError`; `body` always carries the raw response text.
    """

    def __init__(self, *, response: httpx.Response, error: ApiError | None) -> None:
        detail = f" — {error.type}: {error.message}" if error else ""
        super().__init__(f"{response.status_code} {response.reason_phrase}{detail}")
        self.response = response
        self.status_code = response.status_code
        self.error = error
        self.body = response.text
