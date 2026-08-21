"""Unit tests for Deterministic Reproducibility (Phase 3.9 Part 1B)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_deterministic_reproducibility():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f1",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title="Title",
            description="Desc",
        )
    ]

    ass1, _, _, _, _, _, _, _ = engine.calculate_risk(findings)
    ass2, _, _, _, _, _, _, _ = engine.calculate_risk(findings)

    assert ass1.risk_score == ass2.risk_score
    assert ass1.risk_band == ass2.risk_band
