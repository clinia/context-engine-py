# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import (
    Patient,
    PatientDetail,
    PatientList,
    ReconciliationData,
    ResolutionReport,
)

_PATIENT: TypeAdapter[Patient] = TypeAdapter(Patient)
_PATIENT_DETAIL: TypeAdapter[PatientDetail] = TypeAdapter(PatientDetail)
_PATIENT_LIST: TypeAdapter[PatientList] = TypeAdapter(PatientList)
_RECONCILIATION_DATA_OR_STR: TypeAdapter[ReconciliationData | str] = TypeAdapter(
    ReconciliationData | str
)
_RESOLUTION_REPORT: TypeAdapter[ResolutionReport] = TypeAdapter(ResolutionReport)


class PatientsResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_patients(self, *, page: int | None = None, per_page: int | None = None) -> PatientList:
        """List patients.

        Returns a page of the patients currently registered, ordered by patient ID. An empty
        page is returned if none have been registered yet. Graph counts are read per patient
        from the graph endpoints.
        """
        return self._http.request(
            "GET",
            "/v1/patients",
            query={"page": page, "perPage": per_page},
            cast_to=_PATIENT_LIST,
        )

    def get_patient(self, patient_id: str) -> PatientDetail:
        """Get patient.

        Returns demographic metadata and pipeline stats for a patient identified by its patient
        ID.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=_PATIENT_DETAIL,
        )

    def get_resolution(
        self, patient_id: str, *, page: int | None = None, per_page: int | None = None
    ) -> ResolutionReport:
        """Get resolution report.

        Returns the fact-resolution report for a patient: a paginated list of persisted facts of
        every fact type with their provenance traces, source contributions, field-level conflict
        resolutions, and merge confidence scores. Summary counts always cover the full graph,
        not just the returned page.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/resolution",
            path_params={"patientId": patient_id},
            query={"page": page, "perPage": per_page},
            cast_to=_RESOLUTION_REPORT,
        )

    def get_reconciliation(
        self, patient_id: str, *, format: Literal["json", "markdown"] | None = None
    ) -> ReconciliationData | str:
        """Get reconciliation summary.

        Returns the post-pipeline reconciliation summary including entity merge stats and
        inferred relationships. Defaults to Markdown; pass `?format=json` for structured data.
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/reconciliation",
            path_params={"patientId": patient_id},
            query={"format": format},
            cast_to=_RECONCILIATION_DATA_OR_STR,
        )

    def delete_patient(self, patient_id: str) -> None:
        """Delete patient.

        Removes a patient and all associated entities, events, and relationships from the
        registry. Irreversible.
        """
        return self._http.request(
            "DELETE",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=None,
        )

    def upsert_patient(self, patient_id: str) -> Patient:
        """Upsert patient.

        Creates the patient entry if it does not yet exist, or returns the existing record
        unchanged. Idempotent.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.
        """
        return self._http.request(
            "PUT",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=_PATIENT,
        )


class AsyncPatientsResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_patients(
        self, *, page: int | None = None, per_page: int | None = None
    ) -> PatientList:
        """List patients.

        Returns a page of the patients currently registered, ordered by patient ID. An empty
        page is returned if none have been registered yet. Graph counts are read per patient
        from the graph endpoints.
        """
        return await self._http.request(
            "GET",
            "/v1/patients",
            query={"page": page, "perPage": per_page},
            cast_to=_PATIENT_LIST,
        )

    async def get_patient(self, patient_id: str) -> PatientDetail:
        """Get patient.

        Returns demographic metadata and pipeline stats for a patient identified by its patient
        ID.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=_PATIENT_DETAIL,
        )

    async def get_resolution(
        self, patient_id: str, *, page: int | None = None, per_page: int | None = None
    ) -> ResolutionReport:
        """Get resolution report.

        Returns the fact-resolution report for a patient: a paginated list of persisted facts of
        every fact type with their provenance traces, source contributions, field-level conflict
        resolutions, and merge confidence scores. Summary counts always cover the full graph,
        not just the returned page.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/resolution",
            path_params={"patientId": patient_id},
            query={"page": page, "perPage": per_page},
            cast_to=_RESOLUTION_REPORT,
        )

    async def get_reconciliation(
        self, patient_id: str, *, format: Literal["json", "markdown"] | None = None
    ) -> ReconciliationData | str:
        """Get reconciliation summary.

        Returns the post-pipeline reconciliation summary including entity merge stats and
        inferred relationships. Defaults to Markdown; pass `?format=json` for structured data.
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/reconciliation",
            path_params={"patientId": patient_id},
            query={"format": format},
            cast_to=_RECONCILIATION_DATA_OR_STR,
        )

    async def delete_patient(self, patient_id: str) -> None:
        """Delete patient.

        Removes a patient and all associated entities, events, and relationships from the
        registry. Irreversible.
        """
        return await self._http.request(
            "DELETE",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=None,
        )

    async def upsert_patient(self, patient_id: str) -> Patient:
        """Upsert patient.

        Creates the patient entry if it does not yet exist, or returns the existing record
        unchanged. Idempotent.

        New ids are limited to `[A-Za-z0-9][A-Za-z0-9.~:-]{0,127}`, but you can keep referring
        to previous ids as they were defined.
        """
        return await self._http.request(
            "PUT",
            "/v1/patients/{patientId}",
            path_params={"patientId": patient_id},
            cast_to=_PATIENT,
        )
