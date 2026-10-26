# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Any, Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import AppendMessagesBody, Session, SessionMemoryList

_SESSION: TypeAdapter[Session] = TypeAdapter(Session)
_SESSION_MEMORY_LIST: TypeAdapter[SessionMemoryList] = TypeAdapter(SessionMemoryList)
_DICT: TypeAdapter[dict[str, Any]] = TypeAdapter(dict[str, Any])


class SessionsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_session_memories(
        self,
        patient_id: str,
        session_id: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
        sort: Literal["createdAt"] | None = None,
        order: Literal["asc", "desc"] | None = None,
    ) -> SessionMemoryList:
        """List session memories.

        Returns the memories extracted from this session, paginated. Sorted by `createdAt`
        descending (newest first) by default.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            query={"page": page, "perPage": per_page, "sort": sort, "order": order},
            cast_to=_SESSION_MEMORY_LIST,
        )

    def create_session(self, patient_id: str) -> Session:
        """Create session.

        Opens a new query session scoped to a patient. Sessions track interaction context across
        multiple MCP tool calls within a single agent run.

        Deprecated: a session no longer needs opening. Writing under a `sessionId` of your
        choosing — appending messages, a tool call's `session_id`, or `POST
        …/ingestions/sessions` — creates it, and the import route generates one when a
        transcript declares none.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions",
            path_params={"patientId": patient_id},
            cast_to=_SESSION,
        )

    def get_session(self, patient_id: str, session_id: str) -> Session:
        """Get session.

        Returns metadata for a session.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/sessions/{sessionId}",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_SESSION,
        )

    def upsert_session(self, patient_id: str, session_id: str) -> Session:
        """Upsert a session.

        Idempotently opens a session under a caller-provided id: creates it if new, or returns
        the existing session unchanged. Sessions track interaction context across multiple MCP
        tool calls within a single agent run.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.

        Deprecated: a session no longer needs opening. Its first write — appending messages, a
        tool call's `session_id`, or `POST …/ingestions/sessions` — creates it.
        """
        return self._http.request(
            "PUT",
            "/v1/patients/{patientId}/sessions/{sessionId}",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_SESSION,
        )

    def append_messages(
        self, patient_id: str, session_id: str, body: AppendMessagesBody | dict[str, Any]
    ) -> dict[str, Any]:
        """Append session messages.

        Appends user/assistant messages to a session, in order, creating the session if this is
        its first write, and queues memory formation over them. The returned `ingestion` is the
        receipt to poll. Tool-call turns are recorded separately by the MCP layer and are not
        accepted here.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.

        Deprecated: use `POST …/ingestions/sessions`, which accepts the same messages under the
        session's id.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/messages",
            path_params={"patientId": patient_id, "sessionId": session_id},
            json=body,
            cast_to=_DICT,
        )

    def generate_memories(self, patient_id: str, session_id: str) -> dict[str, Any]:
        """Generate session memories.

        Accepts and does nothing: memories form from a session's messages as they arrive,
        through appending messages or `POST …/ingestions/sessions`, each of which returns the
        ingestion receipt to poll. `GET …/memories` returns a session's memories as they land.

        Deprecated: drop the call.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_DICT,
        )


class AsyncSessionsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_session_memories(
        self,
        patient_id: str,
        session_id: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
        sort: Literal["createdAt"] | None = None,
        order: Literal["asc", "desc"] | None = None,
    ) -> SessionMemoryList:
        """List session memories.

        Returns the memories extracted from this session, paginated. Sorted by `createdAt`
        descending (newest first) by default.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            query={"page": page, "perPage": per_page, "sort": sort, "order": order},
            cast_to=_SESSION_MEMORY_LIST,
        )

    async def create_session(self, patient_id: str) -> Session:
        """Create session.

        Opens a new query session scoped to a patient. Sessions track interaction context across
        multiple MCP tool calls within a single agent run.

        Deprecated: a session no longer needs opening. Writing under a `sessionId` of your
        choosing — appending messages, a tool call's `session_id`, or `POST
        …/ingestions/sessions` — creates it, and the import route generates one when a
        transcript declares none.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions",
            path_params={"patientId": patient_id},
            cast_to=_SESSION,
        )

    async def get_session(self, patient_id: str, session_id: str) -> Session:
        """Get session.

        Returns metadata for a session.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/sessions/{sessionId}",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_SESSION,
        )

    async def upsert_session(self, patient_id: str, session_id: str) -> Session:
        """Upsert a session.

        Idempotently opens a session under a caller-provided id: creates it if new, or returns
        the existing session unchanged. Sessions track interaction context across multiple MCP
        tool calls within a single agent run.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.

        Deprecated: a session no longer needs opening. Its first write — appending messages, a
        tool call's `session_id`, or `POST …/ingestions/sessions` — creates it.
        """
        return await self._http.request(
            "PUT",
            "/v1/patients/{patientId}/sessions/{sessionId}",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_SESSION,
        )

    async def append_messages(
        self, patient_id: str, session_id: str, body: AppendMessagesBody | dict[str, Any]
    ) -> dict[str, Any]:
        """Append session messages.

        Appends user/assistant messages to a session, in order, creating the session if this is
        its first write, and queues memory formation over them. The returned `ingestion` is the
        receipt to poll. Tool-call turns are recorded separately by the MCP layer and are not
        accepted here.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.

        Deprecated: use `POST …/ingestions/sessions`, which accepts the same messages under the
        session's id.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/messages",
            path_params={"patientId": patient_id, "sessionId": session_id},
            json=body,
            cast_to=_DICT,
        )

    async def generate_memories(self, patient_id: str, session_id: str) -> dict[str, Any]:
        """Generate session memories.

        Accepts and does nothing: memories form from a session's messages as they arrive,
        through appending messages or `POST …/ingestions/sessions`, each of which returns the
        ingestion receipt to poll. `GET …/memories` returns a session's memories as they land.

        Deprecated: drop the call.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_DICT,
        )
