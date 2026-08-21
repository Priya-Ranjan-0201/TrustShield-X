"""Unit tests for Network-Heavy Legitimate Application Scenarios (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_network_heavy_app_bounded_risk():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id=f"f_net_{i}",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title=f"Endpoint {i}",
            description=f"Description {i}",
        )
        for i in range(10)
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_score <= 100.0
