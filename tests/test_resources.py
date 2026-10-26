"""Request shapes the generator has to get right on its own: a body that is
not JSON, a query parameter whose type sits behind a `$ref`, and the parsing
seams of the shared core (error envelope, content-type-dependent responses)."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from pydantic import ValidationError

from clinia_context_engine import (
    APIStatusError,
    AsyncContextEngineClient,
    ContextEngineClient,
    resources,
)
from clinia_context_engine.generated.models import (
    AppendMessagesBody,
    ChunkedIntoEdge,
    LearnedMemoryNode,
    Message,
    ReconciliationData,
)

INGESTION = {
    "ingestionId": "ing_1",
    "source": "cda/r2",
    "mimeType": "application/cda+xml",
    "receivedAt": "2026-01-01T00:00:00Z",
    "status": "pending",
    "staged": {"facts": 0, "events": 0, "narratives": 0, "messages": 0},
    "startedAt": None,
    "completedAt": None,
    "failure": None,
}


def capture(payload: dict[str, Any] | list[Any], status_code: int = 200):
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(status_code, json=payload)

    transport = httpx.MockTransport(handler)
    client = ContextEngineClient(
        base_url="http://engine.test", http_client=httpx.Client(transport=transport)
    )
    return client, sent


def test_cda_document_posted_as_xml_not_json_string() -> None:
    xml = '<?xml version="1.0"?><ClinicalDocument/>'
    client, sent = capture(INGESTION)

    client.ingest.ingest_cda_r2("patient-1", xml)

    [request] = sent
    assert request.headers["Content-Type"] == "application/cda+xml"
    # A JSON serializer would send `"<?xml …/>"` — quoted, escaped, and
    # unparseable as a document.
    assert request.content.decode() == xml


def test_every_requested_status_sent_on_ingestions_filter() -> None:
    client, sent = capture({"data": [], "meta": {"total": 0, "page": 0, "perPage": 1}})

    client.ingest.list_ingestions("patient-1", status=["pending", "processing"], per_page=1)

    params = sent[0].url.params
    assert params.get_list("status") == ["pending", "processing"]
    assert params["perPage"] == "1"


def test_omitted_query_params_are_not_sent() -> None:
    client, sent = capture({"data": [], "meta": {"total": 0, "page": 0, "perPage": 100}})

    client.ingest.list_ingestions("patient-1")

    assert str(sent[0].url) == "http://engine.test/v1/patients/patient-1/ingestions"


def test_reconciliation_markdown_comes_back_as_text() -> None:
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(200, text="# Reconciliation", headers={"Content-Type": "text/plain"})

    client = ContextEngineClient(
        base_url="http://engine.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    result = client.patients.get_reconciliation("patient-1")

    assert result == "# Reconciliation"


def test_reconciliation_json_comes_back_as_model() -> None:
    payload: dict[str, Any] = {
        "patientName": "Jane Doe",
        "stats": {
            "inputEntities": 0,
            "resolvedEntities": 0,
            "mergedGroups": 0,
            "explicitRelationships": 0,
            "inferredRelationships": 0,
        },
        "mergedEntities": [],
        "inferredRelationships": [],
    }
    client, _ = capture(payload)

    result = client.patients.get_reconciliation("patient-1", format="json")

    assert isinstance(result, ReconciliationData)
    assert result.patient_name == "Jane Doe"


def test_node_union_response_resolves_to_its_variant() -> None:
    payload: dict[str, Any] = {
        "type": "learned_memory",
        "id": "lm_1",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
        "payload": {"type": "symptom", "content": "Headaches at night", "sessionId": "ses_1"},
    }
    client, _ = capture(payload)

    node = client.graph.get_node("patient-1", "learned_memory", "lm_1")

    assert isinstance(node, LearnedMemoryNode)
    assert node.payload.content == "Headaches at night"


def test_edge_union_response_resolves_to_its_variant() -> None:
    payload: dict[str, Any] = {
        "type": "chunked_into",
        "id": "ci_1",
        "createdAt": "2026-01-01T00:00:00Z",
        "updatedAt": "2026-01-01T00:00:00Z",
        "from": {"id": "en_1", "type": "extracted_narrative"},
        "to": {"id": "np_1", "type": "narrative_passage"},
        "payload": {},
    }
    client, _ = capture(payload)

    edge = client.graph.get_edge("patient-1", "chunked_into", "ci_1")

    assert isinstance(edge, ChunkedIntoEdge)


def test_session_response_parses_as_the_session_model() -> None:
    # A request body's inline item once took the `Session` name, and every session
    # method then rejected the server's real response.
    client, _ = capture(
        {"sessionId": "chat-1", "patientId": "patient-1", "createdAt": "2026-01-01T00:00:00Z"}
    )

    session = client.sessions.upsert_session("patient-1", "chat-1")

    assert session.session_id == "chat-1"


def test_ingest_sessions_returns_each_session_id_on_intake() -> None:
    client, sent = capture(
        {
            **INGESTION,
            "source": "session/v1",
            "mimeType": "application/json",
            "intake": [
                {
                    "unit": "message",
                    "received": 1,
                    "entries": [{"kind": "user", "count": 1, "outcome": "text_only"}],
                    "sessionId": "chat-1",
                }
            ],
        },
        status_code=202,
    )

    receipt = client.ingest.ingest_sessions(
        "patient-1",
        {"sessions": [{"sessionId": "chat-1", "messages": [{"role": "user", "content": "hi"}]}]},
    )

    assert json.loads(sent[0].content)["sessions"][0]["sessionId"] == "chat-1"
    assert receipt.intake is not None
    assert receipt.intake[0].session_id == "chat-1"


def test_empty_response_returns_none() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(204)

    client = ContextEngineClient(
        base_url="http://engine.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    assert client.patients.delete_patient("patient-1") is None


def test_text_response_to_a_json_only_operation_raises() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text="<html></html>", headers={"Content-Type": "text/html"})

    client = ContextEngineClient(
        base_url="http://engine.test",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    with pytest.raises(ValidationError):
        client.patients.get_patient("patient-1")


def test_non_2xx_raises_with_parsed_error_envelope() -> None:
    client, _ = capture(
        {"code": 404, "type": "NOT_FOUND", "message": "no such patient"}, status_code=404
    )

    with pytest.raises(APIStatusError) as exc_info:
        client.patients.get_patient("missing")

    err = exc_info.value
    assert err.status_code == 404
    assert err.error is not None
    assert err.error.type == "NOT_FOUND"
    assert "no such patient" in str(err)


def test_model_bodies_serialize_like_their_wire_shape() -> None:
    client, sent = capture({"ok": True, "messageCount": 1})

    client.sessions.append_messages(
        "patient-1",
        "session-1",
        AppendMessagesBody(messages=[Message(role="user", content="hi")]),
    )

    assert json.loads(sent[0].content) == {"messages": [{"role": "user", "content": "hi"}]}


def test_facade_attaches_every_generated_resource() -> None:
    client = ContextEngineClient(base_url="http://engine.test")
    async_client = AsyncContextEngineClient(base_url="http://engine.test")

    for name in resources.__all__:
        is_async = name.startswith("Async")
        attr = name.removeprefix("Async").removesuffix("Resource").lower()
        facade = async_client if is_async else client
        assert isinstance(getattr(facade, attr), getattr(resources, name))


async def test_async_client_sends_the_same_requests() -> None:
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(200, json=INGESTION)

    async with AsyncContextEngineClient(
        base_url="http://engine.test",
        http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
    ) as client:
        result = await client.ingest.ingest_cda_r2("patient-1", "<ClinicalDocument/>")

    assert result.ingestion_id == "ing_1"
    assert sent[0].headers["Content-Type"] == "application/cda+xml"


def test_bearer_token_attached_per_request() -> None:
    sent: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        sent.append(request)
        return httpx.Response(
            200, json={"name": "engine", "status": "healthy", "version": version_payload()}
        )

    def version_payload() -> dict[str, str]:
        return {"number": "0.0.0", "buildSha": "unknown", "buildDate": "unknown"}

    client = ContextEngineClient(
        base_url="http://engine.test",
        auth=lambda: "tok-123",
        http_client=httpx.Client(transport=httpx.MockTransport(handler)),
    )

    client.info.get_service_info()

    assert sent[0].headers["Authorization"] == "Bearer tok-123"


def test_path_params_are_url_quoted() -> None:
    client, sent = capture(INGESTION)

    client.ingest.get_ingestion("patient-1", "a/b c")

    assert "/ingestions/a%2Fb%20c" in str(sent[0].url)


def test_serialized_json_round_trips() -> None:
    client, sent = capture({"ok": True, "messageCount": 1})

    result = client.sessions.append_messages(
        "patient-1", "session-1", {"messages": [{"role": "user", "content": "hi"}]}
    )

    assert json.loads(sent[0].content) == {"messages": [{"role": "user", "content": "hi"}]}
    assert sent[0].headers["Content-Type"] == "application/json"
    assert result == {"ok": True, "messageCount": 1}
