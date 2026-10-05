from __future__ import annotations

import httpx

from ._auth import (
    AsyncClientCredentialsTokenProvider,
    ClientCredentials,
    ClientCredentialsTokenProvider,
)
from ._http import AsyncHttpClient, AsyncTokenProvider, HttpClient, TokenProvider
from .resources import (
    AsyncGraphResource,
    AsyncInfoResource,
    AsyncIngestResource,
    AsyncPatientsResource,
    AsyncSessionsResource,
    AsyncVFSResource,
    GraphResource,
    InfoResource,
    IngestResource,
    PatientsResource,
    SessionsResource,
    VFSResource,
)

__all__ = ["AsyncContextEngineClient", "ContextEngineClient"]


class ContextEngineClient:
    """Synchronous client for the Context Engine API.

    `auth` accepts either a `ClientCredentials` config — the common case, the
    client then handles token acquisition, caching, and refresh — or a token
    callable for full control (a token from elsewhere, a different grant, or a
    custom refresh strategy), called per request and attached as
    `Authorization: Bearer <token>`. Omit for an unsecured server.

    Owns network resources; use it as a context manager or call `close()`.
    """

    def __init__(
        self,
        *,
        base_url: str,
        auth: ClientCredentials | TokenProvider | None = None,
        timeout: float | httpx.Timeout | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        token_provider: TokenProvider | None
        if isinstance(auth, ClientCredentials):
            token_provider = ClientCredentialsTokenProvider(auth)
        else:
            token_provider = auth

        self.http = HttpClient(
            base_url=base_url,
            token_provider=token_provider,
            timeout=timeout,
            http_client=http_client,
        )
        self.graph = GraphResource(self.http)
        self.info = InfoResource(self.http)
        self.ingest = IngestResource(self.http)
        self.patients = PatientsResource(self.http)
        self.sessions = SessionsResource(self.http)
        self.vfs = VFSResource(self.http)

    def close(self) -> None:
        self.http.close()

    def __enter__(self) -> ContextEngineClient:
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


class AsyncContextEngineClient:
    """Async twin of `ContextEngineClient`."""

    def __init__(
        self,
        *,
        base_url: str,
        auth: ClientCredentials | AsyncTokenProvider | None = None,
        timeout: float | httpx.Timeout | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        token_provider: AsyncTokenProvider | None
        if isinstance(auth, ClientCredentials):
            token_provider = AsyncClientCredentialsTokenProvider(auth)
        else:
            token_provider = auth

        self.http = AsyncHttpClient(
            base_url=base_url,
            token_provider=token_provider,
            timeout=timeout,
            http_client=http_client,
        )
        self.graph = AsyncGraphResource(self.http)
        self.info = AsyncInfoResource(self.http)
        self.ingest = AsyncIngestResource(self.http)
        self.patients = AsyncPatientsResource(self.http)
        self.sessions = AsyncSessionsResource(self.http)
        self.vfs = AsyncVFSResource(self.http)

    async def aclose(self) -> None:
        await self.http.aclose()

    async def __aenter__(self) -> AsyncContextEngineClient:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()
