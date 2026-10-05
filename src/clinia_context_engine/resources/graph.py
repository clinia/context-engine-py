# This file is auto-generated. Do not edit manually.
# Generated from the Context Engine OpenAPI spec.

from __future__ import annotations

from typing import Any, Literal

from pydantic import TypeAdapter

from .._http import AsyncHttpClient, HttpClient
from ..generated.models import (
    ChunkedIntoEdgeList,
    Edge,
    EdgeList,
    ExtractedClinicalEventNodeList,
    ExtractedFactNodeList,
    ExtractedNarrativeNodeList,
    FactNodeList,
    LearnedMemoryNodeList,
    NarrativeNodeList,
    NarrativePassageNodeList,
    Node,
    NodeList,
    RelationshipEdgeList,
    ResolutionDecisionEdgeList,
    ResolvesToEdgeList,
)

_CHUNKED_INTO_EDGE_LIST: TypeAdapter[ChunkedIntoEdgeList] = TypeAdapter(ChunkedIntoEdgeList)
_EDGE: TypeAdapter[Edge] = TypeAdapter(Edge)
_EDGE_LIST: TypeAdapter[EdgeList] = TypeAdapter(EdgeList)
_EXTRACTED_CLINICAL_EVENT_NODE_LIST: TypeAdapter[ExtractedClinicalEventNodeList] = TypeAdapter(
    ExtractedClinicalEventNodeList
)
_EXTRACTED_FACT_NODE_LIST: TypeAdapter[ExtractedFactNodeList] = TypeAdapter(ExtractedFactNodeList)
_EXTRACTED_NARRATIVE_NODE_LIST: TypeAdapter[ExtractedNarrativeNodeList] = TypeAdapter(
    ExtractedNarrativeNodeList
)
_FACT_NODE_LIST: TypeAdapter[FactNodeList] = TypeAdapter(FactNodeList)
_LEARNED_MEMORY_NODE_LIST: TypeAdapter[LearnedMemoryNodeList] = TypeAdapter(LearnedMemoryNodeList)
_NARRATIVE_NODE_LIST: TypeAdapter[NarrativeNodeList] = TypeAdapter(NarrativeNodeList)
_NARRATIVE_PASSAGE_NODE_LIST: TypeAdapter[NarrativePassageNodeList] = TypeAdapter(
    NarrativePassageNodeList
)
_NODE: TypeAdapter[Node] = TypeAdapter(Node)
_NODE_LIST: TypeAdapter[NodeList] = TypeAdapter(NodeList)
_RELATIONSHIP_EDGE_LIST: TypeAdapter[RelationshipEdgeList] = TypeAdapter(RelationshipEdgeList)
_RESOLUTION_DECISION_EDGE_LIST: TypeAdapter[ResolutionDecisionEdgeList] = TypeAdapter(
    ResolutionDecisionEdgeList
)
_RESOLVES_TO_EDGE_LIST: TypeAdapter[ResolvesToEdgeList] = TypeAdapter(ResolvesToEdgeList)


class GraphResource:
    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list_nodes(
        self,
        patient_id: str,
        type: Literal[
            "extracted_fact",
            "fact",
            "extracted_narrative",
            "narrative_passage",
            "narrative",
            "learned_memory",
            "extracted_clinical_event",
        ],
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> NodeList:
        """List nodes.

        Returns a paginated list of nodes of one type from the patient context graph
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/nodes/{type}/items",
            path_params={"patientId": patient_id, "type": type},
            query={"page": page, "perPage": per_page},
            cast_to=_NODE_LIST,
        )

    def list_edges(
        self,
        patient_id: str,
        type: Literal["resolution_decision", "resolves_to", "chunked_into", "relationship"],
        *,
        page: int | None = None,
        per_page: int | None = None,
        touching: str | list[str] | None = None,
    ) -> EdgeList:
        """List edges.

        Returns a paginated list of edges of one type from the patient context graph
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/edges/{type}/items",
            path_params={"patientId": patient_id, "type": type},
            query={"page": page, "perPage": per_page, "touching": touching},
            cast_to=_EDGE_LIST,
        )

    def get_node(
        self,
        patient_id: str,
        type: Literal[
            "extracted_fact",
            "fact",
            "extracted_narrative",
            "narrative_passage",
            "narrative",
            "learned_memory",
            "extracted_clinical_event",
        ],
        node_id: str,
    ) -> Node:
        """Get node.

        Returns a single node from the patient context graph by id
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/nodes/{type}/items/{nodeId}",
            path_params={"patientId": patient_id, "type": type, "nodeId": node_id},
            cast_to=_NODE,
        )

    def get_edge(
        self,
        patient_id: str,
        type: Literal["resolution_decision", "resolves_to", "chunked_into", "relationship"],
        edge_id: str,
    ) -> Edge:
        """Get edge.

        Returns a single edge from the patient context graph by id
        """
        return self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/edges/{type}/items/{edgeId}",
            path_params={"patientId": patient_id, "type": type, "edgeId": edge_id},
            cast_to=_EDGE,
        )

    def query_extracted_fact_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedFactNodeList:
        """Query extracted_fact nodes.

        Returns a paginated, filtered, and sorted page of `extracted_fact` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_fact/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_FACT_NODE_LIST,
        )

    def query_fact_nodes(self, patient_id: str, body: dict[str, Any]) -> FactNodeList:
        """Query fact nodes.

        Returns a paginated, filtered, and sorted page of `fact` nodes from the patient context
        graph — the structured counterpart to `list-nodes`, for conditions that don't fit
        query-string params. `filter` and `sort` narrow to the fields this type declares; see
        the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/fact/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_FACT_NODE_LIST,
        )

    def query_extracted_narrative_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedNarrativeNodeList:
        """Query extracted_narrative nodes.

        Returns a paginated, filtered, and sorted page of `extracted_narrative` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_narrative/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_NARRATIVE_NODE_LIST,
        )

    def query_narrative_passage_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> NarrativePassageNodeList:
        """Query narrative_passage nodes.

        Returns a paginated, filtered, and sorted page of `narrative_passage` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/narrative_passage/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_NARRATIVE_PASSAGE_NODE_LIST,
        )

    def query_narrative_nodes(self, patient_id: str, body: dict[str, Any]) -> NarrativeNodeList:
        """Query narrative nodes.

        Returns a paginated, filtered, and sorted page of `narrative` nodes from the patient
        context graph — the structured counterpart to `list-nodes`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/narrative/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_NARRATIVE_NODE_LIST,
        )

    def query_learned_memory_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> LearnedMemoryNodeList:
        """Query learned_memory nodes.

        Returns a paginated, filtered, and sorted page of `learned_memory` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/learned_memory/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_LEARNED_MEMORY_NODE_LIST,
        )

    def query_extracted_clinical_event_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedClinicalEventNodeList:
        """Query extracted_clinical_event nodes.

        Returns a paginated, filtered, and sorted page of `extracted_clinical_event` nodes from
        the patient context graph — the structured counterpart to `list-nodes`, for conditions
        that don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_clinical_event/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_CLINICAL_EVENT_NODE_LIST,
        )

    def query_resolution_decision_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> ResolutionDecisionEdgeList:
        """Query resolution_decision edges.

        Returns a paginated, filtered, and sorted page of `resolution_decision` edges from the
        patient context graph — the structured counterpart to `list-edges`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/resolution_decision/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RESOLUTION_DECISION_EDGE_LIST,
        )

    def query_resolves_to_edges(self, patient_id: str, body: dict[str, Any]) -> ResolvesToEdgeList:
        """Query resolves_to edges.

        Returns a paginated, filtered, and sorted page of `resolves_to` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/resolves_to/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RESOLVES_TO_EDGE_LIST,
        )

    def query_chunked_into_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> ChunkedIntoEdgeList:
        """Query chunked_into edges.

        Returns a paginated, filtered, and sorted page of `chunked_into` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/chunked_into/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_CHUNKED_INTO_EDGE_LIST,
        )

    def query_relationship_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> RelationshipEdgeList:
        """Query relationship edges.

        Returns a paginated, filtered, and sorted page of `relationship` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/relationship/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RELATIONSHIP_EDGE_LIST,
        )


class AsyncGraphResource:
    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def list_nodes(
        self,
        patient_id: str,
        type: Literal[
            "extracted_fact",
            "fact",
            "extracted_narrative",
            "narrative_passage",
            "narrative",
            "learned_memory",
            "extracted_clinical_event",
        ],
        *,
        page: int | None = None,
        per_page: int | None = None,
    ) -> NodeList:
        """List nodes.

        Returns a paginated list of nodes of one type from the patient context graph
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/nodes/{type}/items",
            path_params={"patientId": patient_id, "type": type},
            query={"page": page, "perPage": per_page},
            cast_to=_NODE_LIST,
        )

    async def list_edges(
        self,
        patient_id: str,
        type: Literal["resolution_decision", "resolves_to", "chunked_into", "relationship"],
        *,
        page: int | None = None,
        per_page: int | None = None,
        touching: str | list[str] | None = None,
    ) -> EdgeList:
        """List edges.

        Returns a paginated list of edges of one type from the patient context graph
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/edges/{type}/items",
            path_params={"patientId": patient_id, "type": type},
            query={"page": page, "perPage": per_page, "touching": touching},
            cast_to=_EDGE_LIST,
        )

    async def get_node(
        self,
        patient_id: str,
        type: Literal[
            "extracted_fact",
            "fact",
            "extracted_narrative",
            "narrative_passage",
            "narrative",
            "learned_memory",
            "extracted_clinical_event",
        ],
        node_id: str,
    ) -> Node:
        """Get node.

        Returns a single node from the patient context graph by id
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/nodes/{type}/items/{nodeId}",
            path_params={"patientId": patient_id, "type": type, "nodeId": node_id},
            cast_to=_NODE,
        )

    async def get_edge(
        self,
        patient_id: str,
        type: Literal["resolution_decision", "resolves_to", "chunked_into", "relationship"],
        edge_id: str,
    ) -> Edge:
        """Get edge.

        Returns a single edge from the patient context graph by id
        """
        return await self._http.request(
            "GET",
            "/v1/patients/{patientId}/graph/edges/{type}/items/{edgeId}",
            path_params={"patientId": patient_id, "type": type, "edgeId": edge_id},
            cast_to=_EDGE,
        )

    async def query_extracted_fact_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedFactNodeList:
        """Query extracted_fact nodes.

        Returns a paginated, filtered, and sorted page of `extracted_fact` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_fact/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_FACT_NODE_LIST,
        )

    async def query_fact_nodes(self, patient_id: str, body: dict[str, Any]) -> FactNodeList:
        """Query fact nodes.

        Returns a paginated, filtered, and sorted page of `fact` nodes from the patient context
        graph — the structured counterpart to `list-nodes`, for conditions that don't fit
        query-string params. `filter` and `sort` narrow to the fields this type declares; see
        the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/fact/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_FACT_NODE_LIST,
        )

    async def query_extracted_narrative_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedNarrativeNodeList:
        """Query extracted_narrative nodes.

        Returns a paginated, filtered, and sorted page of `extracted_narrative` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_narrative/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_NARRATIVE_NODE_LIST,
        )

    async def query_narrative_passage_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> NarrativePassageNodeList:
        """Query narrative_passage nodes.

        Returns a paginated, filtered, and sorted page of `narrative_passage` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/narrative_passage/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_NARRATIVE_PASSAGE_NODE_LIST,
        )

    async def query_narrative_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> NarrativeNodeList:
        """Query narrative nodes.

        Returns a paginated, filtered, and sorted page of `narrative` nodes from the patient
        context graph — the structured counterpart to `list-nodes`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/narrative/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_NARRATIVE_NODE_LIST,
        )

    async def query_learned_memory_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> LearnedMemoryNodeList:
        """Query learned_memory nodes.

        Returns a paginated, filtered, and sorted page of `learned_memory` nodes from the
        patient context graph — the structured counterpart to `list-nodes`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/learned_memory/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_LEARNED_MEMORY_NODE_LIST,
        )

    async def query_extracted_clinical_event_nodes(
        self, patient_id: str, body: dict[str, Any]
    ) -> ExtractedClinicalEventNodeList:
        """Query extracted_clinical_event nodes.

        Returns a paginated, filtered, and sorted page of `extracted_clinical_event` nodes from
        the patient context graph — the structured counterpart to `list-nodes`, for conditions
        that don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/nodes/extracted_clinical_event/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_EXTRACTED_CLINICAL_EVENT_NODE_LIST,
        )

    async def query_resolution_decision_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> ResolutionDecisionEdgeList:
        """Query resolution_decision edges.

        Returns a paginated, filtered, and sorted page of `resolution_decision` edges from the
        patient context graph — the structured counterpart to `list-edges`, for conditions that
        don't fit query-string params. `filter` and `sort` narrow to the fields this type
        declares; see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/resolution_decision/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RESOLUTION_DECISION_EDGE_LIST,
        )

    async def query_resolves_to_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> ResolvesToEdgeList:
        """Query resolves_to edges.

        Returns a paginated, filtered, and sorted page of `resolves_to` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/resolves_to/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RESOLVES_TO_EDGE_LIST,
        )

    async def query_chunked_into_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> ChunkedIntoEdgeList:
        """Query chunked_into edges.

        Returns a paginated, filtered, and sorted page of `chunked_into` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/chunked_into/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_CHUNKED_INTO_EDGE_LIST,
        )

    async def query_relationship_edges(
        self, patient_id: str, body: dict[str, Any]
    ) -> RelationshipEdgeList:
        """Query relationship edges.

        Returns a paginated, filtered, and sorted page of `relationship` edges from the patient
        context graph — the structured counterpart to `list-edges`, for conditions that don't
        fit query-string params. `filter` and `sort` narrow to the fields this type declares;
        see the request body schema for its vocabulary.
        """
        return await self._http.request(
            "POST",
            "/v1/patients/{patientId}/graph/edges/relationship/query",
            path_params={"patientId": patient_id},
            json=body,
            cast_to=_RELATIONSHIP_EDGE_LIST,
        )
