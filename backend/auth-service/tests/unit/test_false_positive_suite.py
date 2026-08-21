"""Unit tests for False Positive Protection Suite (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_false_positive_prevention():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f_perm",
            finding_type="PERMISSION_CAMERA",
            finding_category="PERMISSION",
            title="Camera Permission Requested",
            description="Legitimate application requesting CAMERA permission",
        )
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_band != "CRITICAL_RISK"
