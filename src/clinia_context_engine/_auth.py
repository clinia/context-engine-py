from __future__ import annotations

import asyncio
import threading
import time
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import urlsplit

import httpx

from ._errors import ContextEngineError

__all__ = [
    "AsyncClientCredentialsTokenProvider",
    "ClientCredentials",
    "ClientCredentialsTokenProvider",
]

# Clinia's authorization server, applied when a config names neither a
# `token_url` nor an `issuer` — so `ClientCredentials(client_id, client_secret)`
# is a complete config for a Clinia workspace.
#
# The resource indicator is only defaulted alongside the token URL: it is an
# RFC 8707 indicator naming Clinia's protected resource, and sending it to
# somebody else's authorization server would be wrong.
CLINIA_OAUTH_TOKEN_URL = "https://console.clinia.cloud/api/auth/oauth2/token"
CLINIA_OAUTH_RESOURCE = "https://console.clinia.cloud"

DEFAULT_EXPIRY_MARGIN = 60.0
# Fallback lifetime when the token endpoint omits `expires_in`.
DEFAULT_TTL = 300.0


@dataclass(frozen=True, kw_only=True)
class ClientCredentials:
    """OAuth2 client-credentials configuration.

    For a Clinia workspace, `client_id` + `client_secret` is enough — the token
    endpoint and `resource` indicator default to Clinia's authorization server.
    Naming an `issuer` instead locates a different authorization server by
    OIDC/OAuth2 discovery; naming a `token_url` points at one explicitly.
    """

    client_id: str
    client_secret: str
    token_url: str | None = None
    issuer: str | None = None
    # Discovery transformation used when `issuer` is given: OIDC (default) or
    # RFC 8414.
    discovery_algorithm: Literal["oidc", "oauth2"] = "oidc"
    # RFC 8707 resource indicator naming the protected resource the token is
    # for.
    resource: str | None = None
    # `audience` parameter used by some IdPs (e.g. Auth0).
    audience: str | None = None
    # Space-delimited scopes.
    scope: str | None = None
    # How the credentials are presented to the token endpoint: `post` (the
    # default, what Clinia's authorization server expects) sends them in the
    # request body; `basic` sends them in the Authorization header
    # (RFC 6749 §2.3.1).
    auth_method: Literal["basic", "post"] = "post"
    # Refresh the token this many seconds before it actually expires, so a
    # token is never handed out mid-flight of expiring.
    expiry_margin: float = DEFAULT_EXPIRY_MARGIN


def _discovery_url(config: ClientCredentials) -> str:
    assert config.issuer is not None
    if config.discovery_algorithm == "oauth2":
        # RFC 8414: the well-known segment is inserted between host and path.
        parts = urlsplit(config.issuer)
        path = parts.path.rstrip("/")
        return f"{parts.scheme}://{parts.netloc}/.well-known/oauth-authorization-server{path}"
    return config.issuer.rstrip("/") + "/.well-known/openid-configuration"


def _token_request_args(config: ClientCredentials, token_endpoint: str) -> dict[str, Any]:
    uses_clinia_auth_server = config.token_url is None and config.issuer is None
    resource = config.resource or (CLINIA_OAUTH_RESOURCE if uses_clinia_auth_server else None)

    data: dict[str, str] = {"grant_type": "client_credentials"}
    if resource:
        data["resource"] = resource
    if config.audience:
        data["audience"] = config.audience
    if config.scope:
        data["scope"] = config.scope

    args: dict[str, Any] = {"url": token_endpoint, "data": data}
    if config.auth_method == "basic":
        args["auth"] = httpx.BasicAuth(config.client_id, config.client_secret)
    else:
        data["client_id"] = config.client_id
        data["client_secret"] = config.client_secret
    return args


def _parse_token_response(response: httpx.Response) -> tuple[str, float]:
    """Returns the access token and the absolute time it should be refreshed."""
    if response.is_error:
        detail: str
        try:
            payload = response.json()
            detail = str(payload.get("error", response.reason_phrase))
            if payload.get("error_description"):
                detail += f" — {payload['error_description']}"
        except ValueError:
            detail = response.reason_phrase
        raise ContextEngineError(
            f"client_credentials token request failed: {response.status_code} {detail}"
        )
    payload = response.json()
    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        raise ContextEngineError(
            "client_credentials token request failed: response carries no access_token"
        )
    ttl = float(payload["expires_in"]) if payload.get("expires_in") else DEFAULT_TTL
    return token, ttl


def _parse_discovery_response(response: httpx.Response) -> str:
    if response.is_error:
        raise ContextEngineError(f"authorization server discovery failed: {response.status_code}")
    endpoint = response.json().get("token_endpoint")
    if not isinstance(endpoint, str) or not endpoint:
        raise ContextEngineError(
            "authorization server discovery failed: metadata carries no token_endpoint"
        )
    return endpoint


class _TokenState:
    """Cached token plus the resolved token endpoint, shared by both providers."""

    def __init__(self, config: ClientCredentials) -> None:
        self.config = config
        # Discovery only when an issuer is named and no explicit endpoint
        # overrides it; with neither, Clinia's endpoint is the default.
        if config.token_url or config.issuer is None:
            self.token_endpoint: str | None = config.token_url or CLINIA_OAUTH_TOKEN_URL
        else:
            self.token_endpoint = None
        self.token: str | None = None
        # Absolute monotonic time at which the cached token is considered stale.
        self.refresh_at = 0.0

    def fresh_token(self) -> str | None:
        if self.token is not None and time.monotonic() < self.refresh_at:
            return self.token
        return None

    def store(self, token: str, ttl: float) -> str:
        self.token = token
        self.refresh_at = time.monotonic() + max(0.0, ttl - self.config.expiry_margin)
        return token


class ClientCredentialsTokenProvider:
    """Callable token provider backed by the OAuth2 client-credentials grant.

    Caches the access token until it is within `expiry_margin` of expiry;
    concurrent callers share one token request. When configured with an
    `issuer`, the authorization server metadata is discovered once and
    memoized.
    """

    def __init__(
        self, config: ClientCredentials, *, http_client: httpx.Client | None = None
    ) -> None:
        self._state = _TokenState(config)
        self._http_client = http_client
        self._lock = threading.Lock()

    def __call__(self) -> str:
        token = self._state.fresh_token()
        if token is not None:
            return token
        with self._lock:
            token = self._state.fresh_token()
            if token is not None:
                return token
            return self._fetch()

    def _fetch(self) -> str:
        client = self._http_client or httpx.Client()
        try:
            if self._state.token_endpoint is None:
                response = client.get(_discovery_url(self._state.config))
                self._state.token_endpoint = _parse_discovery_response(response)
            args = _token_request_args(self._state.config, self._state.token_endpoint)
            token, ttl = _parse_token_response(client.post(**args))
            return self._state.store(token, ttl)
        finally:
            if self._http_client is None:
                client.close()


class AsyncClientCredentialsTokenProvider:
    """Async twin of `ClientCredentialsTokenProvider`."""

    def __init__(
        self, config: ClientCredentials, *, http_client: httpx.AsyncClient | None = None
    ) -> None:
        self._state = _TokenState(config)
        self._http_client = http_client
        self._lock = asyncio.Lock()

    async def __call__(self) -> str:
        token = self._state.fresh_token()
        if token is not None:
            return token
        async with self._lock:
            token = self._state.fresh_token()
            if token is not None:
                return token
            return await self._fetch()

    async def _fetch(self) -> str:
        client = self._http_client or httpx.AsyncClient()
        try:
            if self._state.token_endpoint is None:
                response = await client.get(_discovery_url(self._state.config))
                self._state.token_endpoint = _parse_discovery_response(response)
            args = _token_request_args(self._state.config, self._state.token_endpoint)
            token, ttl = _parse_token_response(await client.post(**args))
            return self._state.store(token, ttl)
        finally:
            if self._http_client is None:
                await client.aclose()
