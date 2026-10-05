# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import BrowseResult, ReadResponse

_BROWSE_RESULT: TypeAdapter[BrowseResult] = TypeAdapter(BrowseResult)
_READ_RESPONSE: TypeAdapter[ReadResponse] = TypeAdapter(ReadResponse)


class VFSResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def browse_vfs(self, patient_id: str, *, path: str | None = None) -> BrowseResult:
        """Browse VFS.

        Lists the contents of a VFS path. Returns directory children with name, type, and
        preview, or file content when the path resolves to a file. Paths are relative to the
        patient root (e.g. `/conditions/active`); the patient is identified by the `patientId`
        route param. Defaults to the root when `path` is omitted.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/vfs",
            path_params={"patientId": patient_id},
            query={"path": path},
            cast_to=_BROWSE_RESULT,
        )

    def read_vfs(
        self,
        patient_id: str,
        *,
        path: str | None = None,
        format: Literal["narrative", "structured", "compact"] | None = None,
        token_budget: int | None = None,
    ) -> ReadResponse:
        """Read VFS path.

        Returns the content of a VFS file at the given path. Three output formats are supported:
        `narrative` (full Markdown, default), `compact` (condensed Markdown), and `structured`
        (machine-readable JSON). Use `token_budget` to cap approximate output length in tokens.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/read",
            path_params={"patientId": patient_id},
            query={"path": path, "format": format, "token_budget": token_budget},
            cast_to=_READ_RESPONSE,
        )


class AsyncVFSResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def browse_vfs(self, patient_id: str, *, path: str | None = None) -> BrowseResult:
        """Browse VFS.

        Lists the contents of a VFS path. Returns directory children with name, type, and
        preview, or file content when the path resolves to a file. Paths are relative to the
        patient root (e.g. `/conditions/active`); the patient is identified by the `patientId`
        route param. Defaults to the root when `path` is omitted.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/vfs",
            path_params={"patientId": patient_id},
            query={"path": path},
            cast_to=_BROWSE_RESULT,
        )

    async def read_vfs(
        self,
        patient_id: str,
        *,
        path: str | None = None,
        format: Literal["narrative", "structured", "compact"] | None = None,
        token_budget: int | None = None,
    ) -> ReadResponse:
        """Read VFS path.

        Returns the content of a VFS file at the given path. Three output formats are supported:
        `narrative` (full Markdown, default), `compact` (condensed Markdown), and `structured`
        (machine-readable JSON). Use `token_budget` to cap approximate output length in tokens.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/read",
            path_params={"patientId": patient_id},
            query={"path": path, "format": format, "token_budget": token_budget},
            cast_to=_READ_RESPONSE,
        )
