"""Unit Tests — Exact Matching (Phase 4.0 Part 5 — Section 9, 90)."""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules.certificate_rules import (
    PackageCorrelationRule,
    HashCorrelationRule,
)


class TestExactMatching:
    def test_exact_package_matching(self):
        pkg_a = CanonicalEntityDTO(
            entity_id="p1",
            entity_type="PACKAGE",
            canonical_value="com.example.malware",
            display_value="com.example.malware",
            normalized_value="com.example.malware",
            value_hash="h1",
        )
        pkg_b = CanonicalEntityDTO(
            entity_id="p2",
            entity_type="PACKAGE",
            canonical_value="com.example.malware",
            display_value="com.example.malware",
            normalized_value="com.example.malware",
            value_hash="h1",
        )

        res = PackageCorrelationRule.evaluate(pkg_a, pkg_b)
        assert res.matched is True
        assert res.relationship_type == "MATCHES"
        assert res.confidence == "VERY_HIGH"

    def test_exact_hash_matching(self):
        h_a = CanonicalEntityDTO(
            entity_id="h1",
            entity_type="HASH",
            canonical_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            display_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            normalized_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            value_hash="v1",
        )
        h_b = CanonicalEntityDTO(
            entity_id="h2",
            entity_type="HASH",
            canonical_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            display_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            normalized_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            value_hash="v1",
        )

        res = HashCorrelationRule.evaluate(h_a, h_b)
        assert res.matched is True
        assert res.relationship_type == "MATCHES"
        assert res.candidate_score == 1.0
