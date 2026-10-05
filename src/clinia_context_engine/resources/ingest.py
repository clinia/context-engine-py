# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Any, Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import IngestFhirBody, Ingestion, IngestionList

_INGESTION: TypeAdapter[Ingestion] = TypeAdapter(Ingestion)
_INGESTION_LIST: TypeAdapter[IngestionList] = TypeAdapter(IngestionList)


class IngestResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_ingestions(
        self,
        patient_id: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
        sort: Literal["receivedAt"] | None = None,
        order: Literal["asc", "desc"] | None = None,
        status: list[Literal["pending", "processing", "succeeded", "partial", "failed"]]
        | None = None,
    ) -> IngestionList:
        """List ingestions.

        This patient's submissions, newest arrival last. `status` is derived per submission from
        the work it started, so filtering on it is also how to ask what is outstanding:
        `?status=pending,processing` returns everything still to settle, and its `meta.total` is
        the count — zero means this patient's data has settled.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/ingestions",
            path_params={"patientId": patient_id},
            query={
                "page": page,
                "perPage": per_page,
                "sort": sort,
                "order": order,
                "status": status,
            },
            cast_to=_INGESTION_LIST,
        )

    def get_ingestion(self, patient_id: str, ingestion_id: str) -> Ingestion:
        """Get an ingestion.

        One submission and where its work stands. `status` is derived from the work the
        submission started, so this is the handle to poll after submitting — it stays valid for
        the life of that work.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/ingestions/{ingestionId}",
            path_params={"patientId": patient_id, "ingestionId": ingestion_id},
            cast_to=_INGESTION,
        )

    def ingest_fhir_r4(self, patient_id: str, body: IngestFhirBody | dict[str, Any]) -> Ingestion:
        """Ingest FHIR R4.

        Submits a FHIR R4 Bundle or a single resource. The response is a receipt: extraction
        continues after it is returned, so poll the ingestion to follow it. The version is part
        of the path because a Bundle does not state which FHIR release it is written against.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/fhir/r4",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_INGESTION,
        )

    def ingest_fhir_r5(self, patient_id: str, body: IngestFhirBody | dict[str, Any]) -> Ingestion:
        """Ingest FHIR R5.

        Submits a FHIR R5 Bundle or a single resource. The response is a receipt: ingestion
        continues after it is returned, so poll the ingestion to follow it. The version is part
        of the path because a Bundle does not state which FHIR release it is written against.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/fhir/r5",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_INGESTION,
        )

    def ingest_cda_r2(self, patient_id: str, content: str) -> Ingestion:
        """Ingest CDA R2.

        Submits CDA R2 documents as XML. Post one document as the request body with
        `Content-Type: application/cda+xml`, or several as `multipart/form-data` with one
        `documents` part per document.

        The response is a receipt: ingestion continues after it is returned, so poll the
        ingestion to follow it. `intake` comes back index-aligned with the documents you sent,
        so it stays clear which document held what — and if any document cannot be parsed the
        whole request is rejected and nothing is stored.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/cda/r2",
            path_params={"patientId": patient_id},
            content=content,
            content_type="application/cda+xml",
            cast_to=_INGESTION,
        )


class AsyncIngestResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_ingestions(
        self,
        patient_id: str,
        *,
        page: int | None = None,
        per_page: int | None = None,
        sort: Literal["receivedAt"] | None = None,
        order: Literal["asc", "desc"] | None = None,
        status: list[Literal["pending", "processing", "succeeded", "partial", "failed"]]
        | None = None,
    ) -> IngestionList:
        """List ingestions.

        This patient's submissions, newest arrival last. `status` is derived per submission from
        the work it started, so filtering on it is also how to ask what is outstanding:
        `?status=pending,processing` returns everything still to settle, and its `meta.total` is
        the count — zero means this patient's data has settled.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/ingestions",
            path_params={"patientId": patient_id},
            query={
                "page": page,
                "perPage": per_page,
                "sort": sort,
                "order": order,
                "status": status,
            },
            cast_to=_INGESTION_LIST,
        )

    async def get_ingestion(self, patient_id: str, ingestion_id: str) -> Ingestion:
        """Get an ingestion.

        One submission and where its work stands. `status` is derived from the work the
        submission started, so this is the handle to poll after submitting — it stays valid for
        the life of that work.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/ingestions/{ingestionId}",
            path_params={"patientId": patient_id, "ingestionId": ingestion_id},
            cast_to=_INGESTION,
        )

    async def ingest_fhir_r4(
        self, patient_id: str, body: IngestFhirBody | dict[str, Any]
    ) -> Ingestion:
        """Ingest FHIR R4.

        Submits a FHIR R4 Bundle or a single resource. The response is a receipt: extraction
        continues after it is returned, so poll the ingestion to follow it. The version is part
        of the path because a Bundle does not state which FHIR release it is written against.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/fhir/r4",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_INGESTION,
        )

    async def ingest_fhir_r5(
        self, patient_id: str, body: IngestFhirBody | dict[str, Any]
    ) -> Ingestion:
        """Ingest FHIR R5.

        Submits a FHIR R5 Bundle or a single resource. The response is a receipt: ingestion
        continues after it is returned, so poll the ingestion to follow it. The version is part
        of the path because a Bundle does not state which FHIR release it is written against.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/fhir/r5",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_INGESTION,
        )

    async def ingest_cda_r2(self, patient_id: str, content: str) -> Ingestion:
        """Ingest CDA R2.

        Submits CDA R2 documents as XML. Post one document as the request body with
        `Content-Type: application/cda+xml`, or several as `multipart/form-data` with one
        `documents` part per document.

        The response is a receipt: ingestion continues after it is returned, so poll the
        ingestion to follow it. `intake` comes back index-aligned with the documents you sent,
        so it stays clear which document held what — and if any document cannot be parsed the
        whole request is rejected and nothing is stored.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/ingestions/cda/r2",
            path_params={"patientId": patient_id},
            content=content,
            content_type="application/cda+xml",
            cast_to=_INGESTION,
        )
