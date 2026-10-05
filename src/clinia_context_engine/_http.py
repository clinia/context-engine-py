from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from typing import Any, TypeVar, overload
from urllib.parse import quote

import httpx
from pydantic import BaseModel, TypeAdapter, ValidationError

from ._errors import APIConnectionError, APIStatusError, APITimeoutError
from .generated.models import ApiError

__all__ = ["AsyncHttpClient", "AsyncTokenProvider", "HttpClient", "TokenProvider"]

TokenProvider = Callable[[], str]
AsyncTokenProvider = Callable[[], Awaitable[str]]

DEFAULT_TIMEOUT = httpx.Timeout(60.0)

T = TypeVar("T")


def _substitute_path(path: str, path_params: Mapping[str, Any] | None) -> str:
    if not path_params:
        return path
    for name, value in path_params.items():
        path = path.replace("{" + name + "}", quote(str(value), safe=""))
    return path


def _prepare_query(query: Mapping[str, Any] | None) -> dict[str, Any] | None:
    """Omitted (None) parameters are dropped rather than sent as empty values."""
    if query is None:
        return None
    prepared = {name: value for name, value in query.items() if value is not None}
    return prepared or None


def _prepare_json(body: Any) -> Any:
    if isinstance(body, BaseModel):
        return body.model_dump(mode="json", by_alias=True, exclude_unset=True)
    return body


def _parse_response(response: httpx.Response, cast_to: TypeAdapter[T] | None) -> T | None:
    if cast_to is None:
        return None
    # Operations that also declare a text response (e.g. a Markdown rendering
    # behind a `format` query parameter) carry `str` in `cast_to`'s union, so a
    # non-JSON response validates as its text.
    if "json" in response.headers.get("Content-Type", ""):
        return cast_to.validate_json(response.content)
    return cast_to.validate_python(response.text)


def _status_error(response: httpx.Response) -> APIStatusError:
    try:
        error = ApiError.model_validate_json(response.content)
    except ValidationError:
        error = None
    return APIStatusError(response=response, error=error)


class _RequestBuilder:
    """Request construction shared by the sync and async clients."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def build_args(
        self,
        method: str,
        path: str,
        *,
        path_params: Mapping[str, Any] | None,
        query: Mapping[str, Any] | None,
        json: Any,
        content: str | bytes | None,
        content_type: str | None,
        token: str | None,
    ) -> dict[str, Any]:
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        if content_type is not None:
            headers["Content-Type"] = content_type

        args: dict[str, Any] = {
            "method": method,
            "url": self._base_url + _substitute_path(path, path_params),
            "headers": headers,
        }
        params = _prepare_query(query)
        if params is not None:
            args["params"] = params
        if json is not None:
            args["json"] = _prepare_json(json)
        if content is not None:
            args["content"] = content
        return args


class HttpClient:
    """Thin typed transport: one `request()` the generated resources call.

    Owns an `httpx.Client` unless one is injected; injected clients are not
    closed by `close()`.
    """

    def __init__(
        self,
        *,
        base_url: str,
        token_provider: TokenProvider | None = None,
        timeout: float | httpx.Timeout | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._builder = _RequestBuilder(base_url)
        self._token_provider = token_provider
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=timeout or DEFAULT_TIMEOUT)

    @overload
    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: TypeAdapter[T],
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> T: ...

    @overload
    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> None: ...

    def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: TypeAdapter[T] | None,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> T | None:
        token = self._token_provider() if self._token_provider else None
        args = self._builder.build_args(
            method,
            path,
            path_params=path_params,
            query=query,
            json=json,
            content=content,
            content_type=content_type,
            token=token,
        )
        try:
            response = self._client.request(**args)
        except httpx.TimeoutException as err:
            raise APITimeoutError(request=err.request) from err
        except httpx.TransportError as err:
            raise APIConnectionError(str(err), request=err.request) from err
        if response.is_error:
            raise _status_error(response)
        return _parse_response(response, cast_to)

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> HttpClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncHttpClient:
    """Async twin of `HttpClient`, backed by `httpx.AsyncClient`."""

    def __init__(
        self,
        *,
        base_url: str,
        token_provider: AsyncTokenProvider | None = None,
        timeout: float | httpx.Timeout | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._builder = _RequestBuilder(base_url)
        self._token_provider = token_provider
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=timeout or DEFAULT_TIMEOUT)

    @overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: TypeAdapter[T],
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> T: ...

    @overload
    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: None,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> None: ...

    async def request(
        self,
        method: str,
        path: str,
        *,
        cast_to: TypeAdapter[T] | None,
        path_params: Mapping[str, Any] | None = None,
        query: Mapping[str, Any] | None = None,
        json: Any = None,
        content: str | bytes | None = None,
        content_type: str | None = None,
    ) -> T | None:
        token = await self._token_provider() if self._token_provider else None
        args = self._builder.build_args(
            method,
            path,
            path_params=path_params,
            query=query,
            json=json,
            content=content,
            content_type=content_type,
            token=token,
        )
        try:
            response = await self._client.request(**args)
        except httpx.TimeoutException as err:
            raise APITimeoutError(request=err.request) from err
        except httpx.TransportError as err:
            raise APIConnectionError(str(err), request=err.request) from err
        if response.is_error:
            raise _status_error(response)
        return _parse_response(response, cast_to)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncHttpClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()
