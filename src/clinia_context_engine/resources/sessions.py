# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Any, Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import AppendMessagesBody, IngestSessionBody, Session, SessionMemoryList

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

        Appends user/assistant messages to an open session, in order. The session stays open.
        Tool-call turns are recorded separately by the MCP layer and are not accepted here.
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

        Extracts memories from messages appended since the last run and infers memory↔fact
        relationships. The session stays active and can keep receiving messages. Append-only: it
        never re-extracts messages already covered by a prior run, so re-running it only adds
        memories for what's new, but it does not deduplicate against memories from a previous
        run. Call it intentionally rather than on every turn.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_DICT,
        )

    def ingest_session(
        self, patient_id: str, body: IngestSessionBody | dict[str, Any]
    ) -> dict[str, Any]:
        """Ingest a complete session.

        Replays a complete set of messages as one session: creates the session, appends every
        message in order, then generates memories from it synchronously, so the response returns
        only after the patient's memories reflect the conversation. Messages can still be
        appended to the session. Intended for batch/replay use, not interactive sessions.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/ingest",
            path_params={"patientId": patient_id},
            json=body,
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

        Appends user/assistant messages to an open session, in order. The session stays open.
        Tool-call turns are recorded separately by the MCP layer and are not accepted here.
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

        Extracts memories from messages appended since the last run and infers memory↔fact
        relationships. The session stays active and can keep receiving messages. Append-only: it
        never re-extracts messages already covered by a prior run, so re-running it only adds
        memories for what's new, but it does not deduplicate against memories from a previous
        run. Call it intentionally rather than on every turn.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/{sessionId}/memories",
            path_params={"patientId": patient_id, "sessionId": session_id},
            cast_to=_DICT,
        )

    async def ingest_session(
        self, patient_id: str, body: IngestSessionBody | dict[str, Any]
    ) -> dict[str, Any]:
        """Ingest a complete session.

        Replays a complete set of messages as one session: creates the session, appends every
        message in order, then generates memories from it synchronously, so the response returns
        only after the patient's memories reflect the conversation. Messages can still be
        appended to the session. Intended for batch/replay use, not interactive sessions.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/sessions/ingest",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_DICT,
        )
