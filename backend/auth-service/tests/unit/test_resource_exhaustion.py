"""Unit tests for Resource Exhaustion Defense (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_resource_exhaustion_large_findings():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id=f"f_res_{i}",
            finding_type="NETWORK_ENDPOINT_OBSERVED",
            finding_category="NETWORK",
            title=f"Title {i}",
            description=f"Description {i}",
        )
        for i in range(500)
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_score <= 100.0
