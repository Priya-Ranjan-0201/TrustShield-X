"""Unit Tests — Relationship Model & Taxonomy (Phase 4.0 Part 5 — Sections 12-16, 90)."""

import pytest
from app.schemas.intelligence_graph_models import GraphRelationshipDTO


class TestRelationshipModel:
    def test_relationship_dto_properties(self):
        rel = GraphRelationshipDTO(
            relationship_id="rel_01",
            source_entity_id="ent_apk",
            target_entity_id="ent_cert",
            relationship_type="USES_CERTIFICATE",
            confidence="VERY_HIGH",
            evidence_strength="STRONG",
            resolution_status="ACTIVE",
            correlation_method="CERT_PARSER",
            correlation_version="1.0.0",
        )
        assert rel.relationship_type == "USES_CERTIFICATE"
        assert rel.confidence == "VERY_HIGH"
        assert rel.status == "ACTIVE"
