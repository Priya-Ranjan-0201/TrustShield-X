"""Unit tests for Duplicate Evidence Attack Bounded Contribution (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_duplicate_evidence_attack_bounded():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f_dup",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title="Duplicate Endpoint",
            description="Same endpoint repeated",
        )
        for _ in range(100)
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_score <= 100.0
