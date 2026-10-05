# clinia-context-engine

Python client for the Clinia Context Engine API. A thin, typed wrapper over
[`httpx`](https://www.python-httpx.org/) with [Pydantic v2](https://docs.pydantic.dev/)
models generated from the OpenAPI contract — resource methods, parameters, and
response models are fully typed, in both sync and async flavors. Requires
Python 3.10+.

## Install

```sh
pip install clinia-context-engine
```

## Usage

Every Clinia workspace requires authentication. Create OAuth credentials in the
[Console](https://console.clinia.cloud) — scoped to your workspace, with **Read &
Write** if you intend to ingest data or create patients — then point `base_url`
at your workspace:

```python
from clinia_context_engine import ClientCredentials, ContextEngineClient

with ContextEngineClient(
    base_url="https://<workspace-id>.w.clinia.cloud",
    auth=ClientCredentials(client_id="your-client-id", client_secret="your-client-secret"),
) as client:
    patients = client.patients.list_patients()
    report = client.patients.get_resolution("patient-123", page=0, per_page=50)
```

That is the whole configuration. The client resolves Clinia's authorization
server, acquires a bearer token, caches it, refreshes it before expiry, and
attaches `Authorization: Bearer <token>` to every request. Tokens last an hour;
you do not manage them.

Methods are grouped by resource (`client.patients`, `client.ingest`,
`client.sessions`, `client.vfs`, `client.graph`, `client.info`) and return
Pydantic models parsed from the response. Field names are `snake_case` in
Python and mapped to the API's wire names automatically.

Non-2xx responses raise `APIStatusError`, carrying the parsed error envelope:

```python
from clinia_context_engine import APIStatusError

try:
    client.patients.get_patient("missing")
except APIStatusError as err:
    print(err.status_code, err.error.type if err.error else err.body)
```

### Async

`AsyncContextEngineClient` is the async twin — same resources, same signatures,
`await`ed:

```python
from clinia_context_engine import AsyncContextEngineClient, ClientCredentials

async with AsyncContextEngineClient(base_url=base_url, auth=credentials) as client:
    patients = await client.patients.list_patients()
```

### Without authentication

Omit `auth` entirely and the client sends no `Authorization` header. Useful
against a server that does not require one — a stub or recorded fixture in your
own tests. An `http://` base URL is fine there. Note this is about the _client_
sending no credentials: a Clinia workspace always requires them, so pointing an
unauthenticated client at one yields 401s on every request rather than a clear
startup failure.

### Bring your own token

For a token you obtained elsewhere, a different grant, or a custom refresh
strategy, pass `auth` a callable instead of a config. It is called per request
and returns the token to attach:

```python
client = ContextEngineClient(base_url=base_url, auth=lambda: token_store.valid_access_token())
```

`ClientCredentialsTokenProvider` (and its async twin) is exactly such a
callable, so one cached provider can be shared across several clients.

### Bring your own httpx client

Pass `http_client` an `httpx.Client` (or `httpx.AsyncClient`) you configured
yourself — proxies, event hooks, a `MockTransport` in tests. A provided client
is not closed by `close()`.

## Options

| Option        | Type                                        | Description                                                                         |
| ------------- | ------------------------------------------- | ----------------------------------------------------------------------------------- |
| `base_url`    | `str`                                       | Context Engine workspace base URL. Required.                                        |
| `auth`        | `ClientCredentials` or `() -> str` callable | OAuth2 client-credentials config (common case) **or** a per-request token callable. |
| `timeout`     | `float` or `httpx.Timeout`                  | Request timeout. Defaults to 60 seconds.                                            |
| `http_client` | `httpx.Client` / `httpx.AsyncClient`        | Preconfigured transport; not closed by the client.                                  |

## Development

This repository is a mirror of each release; every release replaces its
contents, so pull requests cannot be merged here. Report bugs and requests in
[Issues](https://github.com/clinia/context-engine-py/issues).

The client is generated from the Context Engine OpenAPI spec — the Pydantic
models in `generated/` by
[datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator),
and the resource classes in `resources/`.

```sh
uv sync --group dev
uv run --group dev pytest
uv run --group dev pyright
uv run --group dev ruff check src tests
```

## License

[Apache-2.0](LICENSE) © Clinia Health Inc.
