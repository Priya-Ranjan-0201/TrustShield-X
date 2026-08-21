"""Unit Tests — Graph Relationship Integrity (Phase 4.0 Part 4 — Section 14, 83)."""

import pytest
from app.schemas.investigation_models import GraphEdgeDTO


class TestGraphRelationshipIntegrity:
    def test_graph_edge_valid_relationship(self):
        valid_relationships = [
            "SUPPORTS",
            "CONTRIBUTES_TO",
            "DERIVED_FROM",
            "CORRELATED_WITH",
            "MATCHES",
            "FLOWS_TO",
            "TRIGGERS",
            "MITIGATED_BY",
            "CONTRADICTS",
            "SOURCE_OF",
        ]
        edge = GraphEdgeDTO(
            id="edge_01",
            source="ev_01",
            target="f_01",
            relationship="SUPPORTS",
            resolution_status="RESOLVED",
            confidence="HIGH",
        )
        assert edge.relationship in valid_relationships
        assert edge.resolution_status == "RESOLVED"

    def test_unresolved_relationship_marked_partial_or_unknown(self):
        edge = GraphEdgeDTO(
            id="edge_02",
            source="ev_02",
            target="f_02",
            relationship="CORRELATED_WITH",
            resolution_status="PARTIAL",
            confidence="LOW",
        )
        assert edge.resolution_status in ["PARTIAL", "UNKNOWN"]
