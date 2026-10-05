"""End-to-end demo: create a patient, ingest a FHIR bundle, follow the work.

Ingestion is asynchronous. Submitting returns a receipt immediately, and extraction
continues after it — so the interesting half of this script is the polling loop, which
is what any real integration has to write.

Run it against a workspace:

    export CONTEXT_ENGINE_BASE_URL="https://<workspace-id>.w.clinia.cloud"
    export CONTEXT_ENGINE_CLIENT_ID="..."
    export CONTEXT_ENGINE_CLIENT_SECRET="..."
    uv run examples/quickstart.py

Against a server running without auth, set only `CONTEXT_ENGINE_BASE_URL`.

The patient id is fixed, so re-running reuses the same patient rather than filling the
workspace with demo records. `upsert_patient` is idempotent, and a second run of the same
bundle is recognised as a re-delivery rather than ingested twice — set
`CONTEXT_ENGINE_DEMO_PATIENT_ID` to watch the whole cycle again from scratch.
"""

from __future__ import annotations

import os
import sys
import time
from typing import Any

from clinia_context_engine import APIStatusError, ClientCredentials, ContextEngineClient
from clinia_context_engine.generated.models import Ingestion

# Fixed by default so re-running reuses one patient instead of filling the workspace with
# demo records. Override it to watch the full ingestion cycle again from scratch — the same
# bundle against the same patient is correctly recognised as a re-delivery and stages nothing.
PATIENT_ID = os.environ.get("CONTEXT_ENGINE_DEMO_PATIENT_ID", "quickstart-demo-patient")

# Statuses that mean the work has settled. `partial` is terminal too: some of the
# submission landed and some did not, which `failure` explains.
TERMINAL = frozenset({"succeeded", "partial", "failed"})

POLL_INTERVAL_SECONDS = 2.0
POLL_TIMEOUT_SECONDS = 180.0

# A minimal FHIR R4 collection bundle: one condition and one medication. Small enough to
# read at a glance, real enough that extraction has something to resolve.
#
# R4 spells a medication's code `medicationCodeableConcept` at the top level; R5 moved it
# to `medication.concept`. Post this to `ingest_fhir_r5` unchanged and the medication will
# not be read — which is why the release is part of the path rather than sniffed.
BUNDLE: dict[str, Any] = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resource": {
                "resourceType": "Condition",
                "id": "quickstart-condition-1",
                "code": {
                    "text": "Type 2 diabetes mellitus",
                    "coding": [
                        {
                            "system": "http://snomed.info/sct",
                            "code": "44054006",
                            "display": "Diabetes mellitus type 2",
                        }
                    ],
                },
                "clinicalStatus": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                            "code": "active",
                        }
                    ]
                },
                "onsetDateTime": "2018-03-15",
            }
        },
        {
            "resource": {
                "resourceType": "MedicationStatement",
                "id": "quickstart-medication-1",
                "status": "active",
                "medicationCodeableConcept": {
                    "text": "Metformin",
                    "coding": [
                        {
                            "system": "http://www.nlm.nih.gov/research/umls/rxnorm",
                            "code": "860975",
                            "display": "Metformin",
                        }
                    ],
                },
                "effectivePeriod": {"start": "2019-09-01"},
                "dosage": [{"text": "500 mg twice daily", "route": {"text": "Oral"}}],
            }
        },
    ],
}


def build_client() -> ContextEngineClient:
    """Read configuration from the environment, so no secret is ever in this file."""
    base_url = os.environ.get("CONTEXT_ENGINE_BASE_URL")
    if not base_url:
        sys.exit("CONTEXT_ENGINE_BASE_URL is not set. See this file's docstring.")

    client_id = os.environ.get("CONTEXT_ENGINE_CLIENT_ID")
    client_secret = os.environ.get("CONTEXT_ENGINE_CLIENT_SECRET")

    # Both or neither: half a credential pair is a misconfiguration worth catching here
    # rather than as a 401 three calls later.
    if bool(client_id) != bool(client_secret):
        sys.exit("Set both CONTEXT_ENGINE_CLIENT_ID and CONTEXT_ENGINE_CLIENT_SECRET, or neither.")

    auth = (
        ClientCredentials(client_id=client_id, client_secret=client_secret)
        if client_id and client_secret
        else None
    )
    if auth is None:
        print("No credentials set — connecting unauthenticated.")

    return ContextEngineClient(base_url=base_url, auth=auth)


def poll(client: ContextEngineClient, ingestion_id: str) -> Ingestion:
    """Poll until the submission settles, printing each status change.

    Returns the last receipt read. Raises `TimeoutError` if it has not settled inside
    `POLL_TIMEOUT_SECONDS` — a submission can legitimately take a while, but a demo that
    hangs forever teaches nothing.
    """
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    started = time.monotonic()
    previous: str | None = None

    while True:
        ingestion = client.ingest.get_ingestion(PATIENT_ID, ingestion_id)
        status = ingestion.status
        elapsed = time.monotonic() - started

        if status != previous:
            print(f"  [{elapsed:6.1f}s] {status}")
            previous = status

        if status in TERMINAL:
            return ingestion

        if time.monotonic() >= deadline:
            raise TimeoutError(
                f"still {status} after {POLL_TIMEOUT_SECONDS:.0f}s "
                f"(ingestion {ingestion_id} — it may still finish; poll it again)"
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def main() -> int:
    with build_client() as client:
        service = client.info.get_service_info()
        print(f"Connected to {service.name} {service.version.number}\n")

        patient = client.patients.upsert_patient(PATIENT_ID)
        print(f"Patient ready: {patient.id}")

        receipt = client.ingest.ingest_fhir_r4(PATIENT_ID, BUNDLE)
        staged = receipt.staged
        print(
            f"Submitted {receipt.ingestion_id} — "
            f"staged {staged.facts} facts, {staged.events} events, {staged.narratives} narratives"
        )

        # Every count zero means nothing new was staged: either the payload held nothing
        # usable, or an earlier run already stored it. Either way there is no new work to
        # follow, and `status` refers to whatever run owns the content.
        if staged.facts == staged.events == staged.narratives == 0:
            print("Nothing new staged — this content was already ingested. Skipping the poll.")
            return 0

        print("Following the work:")
        final = poll(client, receipt.ingestion_id)

        if final.failure is not None:
            print(f"\nFinished {final.status}: {final.failure.code} — {final.failure.message}")
            return 1

        print(f"\nFinished {final.status}, settled at {final.completed_at}.")

        # What landed, read back through the VFS: the patient root's directory listing.
        browse = client.vfs.browse_vfs(PATIENT_ID, path="/")
        children = ", ".join(child.name for child in browse.children or [])
        print(f"Patient root now holds: {children or '(nothing yet)'}")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except APIStatusError as err:
        detail = err.error.type if err.error else err.body
        sys.exit(f"API error {err.status_code}: {detail}")
    except TimeoutError as err:
        sys.exit(f"Timed out: {err}")
    except KeyboardInterrupt:
        sys.exit(130)
