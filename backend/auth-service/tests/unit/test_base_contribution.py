"""Unit tests for Base Risk Contribution Calculation (Phase 3.9 Part 1B)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_base_contribution_calculation():
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

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert len(factors) == 1
    assert factors[0].base_contribution == 5.0
