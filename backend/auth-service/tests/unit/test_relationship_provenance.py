"""Unit Tests — Relationship Provenance & Explanations (Phase 4.0 Part 5 — Sections 17-18, 90)."""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO, GraphRelationshipDTO
from app.services.graph.correlation_explanation_engine import CorrelationExplanationEngine


class TestRelationshipProvenance:
    def test_relationship_explanation_generation(self):
        rel = GraphRelationshipDTO(
            relationship_id="rel_01",
            source_entity_id="ent_url",
            target_entity_id="ent_dom",
            relationship_type="HOSTS",
            confidence="VERY_HIGH",
            evidence_strength="STRONG",
            resolution_status="ACTIVE",
            correlation_method="URL_PARSER",
            correlation_version="1.0.0",
        )
        src = CanonicalEntityDTO(
            entity_id="ent_url",
            entity_type="URL",
            canonical_value="https://evil.com/login",
            display_value="https://evil.com/login",
            normalized_value="https://evil.com/login",
            value_hash="h1",
        )
        tgt = CanonicalEntityDTO(
            entity_id="ent_dom",
            entity_type="DOMAIN",
            canonical_value="evil.com",
            display_value="evil.com",
            normalized_value="evil.com",
            value_hash="h2",
        )

        exp = CorrelationExplanationEngine.explain(rel, src, tgt)
        assert exp.relationship_id == "rel_01"
        assert "evil.com" in exp.why_connected
        assert len(exp.evidence_signals) > 0
