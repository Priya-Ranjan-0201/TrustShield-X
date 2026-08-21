"""Unit tests for Potentially Unwanted Applications (PUA) Cases (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_pua_case_evaluation():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f_pua",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title="Tracking Domain",
            description="Tracking SDK Endpoint",
        )
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_band in ["TRUSTED", "LOW_RISK"]
