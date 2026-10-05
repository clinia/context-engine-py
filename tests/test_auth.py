from __future__ import annotations

import asyncio

import httpx
import pytest

from clinia_context_engine import (
    AsyncClientCredentialsTokenProvider,
    ClientCredentials,
    ClientCredentialsTokenProvider,
    ContextEngineError,
)
from clinia_context_engine._auth import CLINIA_OAUTH_RESOURCE, CLINIA_OAUTH_TOKEN_URL


def token_transport(
    sent: list[httpx.Request], *, expires_in: int | None = 3600, token: str = "tok"
) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        payload: dict[str, object] = {"access_token": f"{token}-{len(sent)}"}
        if expires_in is not None:
            payload["expires_in"] = expires_in
        return httpx.Response(200, json=payload)

    return httpx.MockTransport(handler)


def test_token_is_cached_until_expiry_margin() -> None:
    sent: list[httpx.Request] = []
    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret"),
        http_client=httpx.Client(transport=token_transport(sent)),
    )

    assert provider() == "tok-1"
    assert provider() == "tok-1"
    assert len(sent) == 1


def test_token_within_expiry_margin_is_refreshed() -> None:
    sent: list[httpx.Request] = []
    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret"),
        http_client=httpx.Client(transport=token_transport(sent, expires_in=30)),
    )

    assert provider() == "tok-1"
    assert provider() == "tok-2"


def test_clinia_defaults_apply_only_without_explicit_endpoint() -> None:
    sent: list[httpx.Request] = []
    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret"),
        http_client=httpx.Client(transport=token_transport(sent)),
    )
    provider()

    assert str(sent[0].url) == CLINIA_OAUTH_TOKEN_URL
    form = dict(httpx.QueryParams(sent[0].content.decode()))
    assert form["resource"] == CLINIA_OAUTH_RESOURCE
    assert form["client_id"] == "cid"
    assert form["client_secret"] == "secret"

    sent.clear()
    provider = ClientCredentialsTokenProvider(
        ClientCredentials(
            client_id="cid", client_secret="secret", token_url="http://idp.test/token"
        ),
        http_client=httpx.Client(transport=token_transport(sent)),
    )
    provider()

    assert str(sent[0].url) == "http://idp.test/token"
    assert "resource" not in dict(httpx.QueryParams(sent[0].content.decode()))


def test_basic_auth_method_uses_authorization_header() -> None:
    sent: list[httpx.Request] = []
    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret", auth_method="basic"),
        http_client=httpx.Client(transport=token_transport(sent)),
    )
    provider()

    assert sent[0].headers["Authorization"].startswith("Basic ")
    form = dict(httpx.QueryParams(sent[0].content.decode()))
    assert "client_secret" not in form


def test_issuer_discovery_resolves_and_memoizes_the_token_endpoint() -> None:
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        if request.url.path.startswith("/.well-known"):
            return httpx.Response(200, json={"token_endpoint": "http://idp.test/oauth/token"})
        return httpx.Response(200, json={"access_token": "tok", "expires_in": 1})

    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret", issuer="http://idp.test"),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    provider()
    provider()  # expired (ttl below margin) — refetches the token, not discovery

    assert [str(r.url) for r in sent] == [
        "http://idp.test/.well-known/openid-configuration",
        "http://idp.test/oauth/token",
        "http://idp.test/oauth/token",
    ]


def test_error_response_raises_with_oauth_detail() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            401, json={"error": "invalid_client", "error_description": "bad secret"}
        )

    provider = ClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret"),
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ContextEngineError, match="invalid_client — bad secret"):
        provider()


async def test_concurrent_async_callers_share_one_token_request() -> None:
    sent: list[httpx.Request] = []
    provider = AsyncClientCredentialsTokenProvider(
        ClientCredentials(client_id="cid", client_secret="secret"),
        http_client=httpx.AsyncClient(transport=token_transport(sent)),
    )

    tokens = await asyncio.gather(*(provider() for _ in range(5)))

    assert set(tokens) == {"tok-1"}
    assert len(sent) == 1
