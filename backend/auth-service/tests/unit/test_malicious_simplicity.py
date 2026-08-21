"""Unit tests for Malicious Simplicity Applications (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_malicious_simplicity_high_risk():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f_simple_mal",
            finding_type="CREDENTIAL_PHISHING_EXFILTRATION",
            finding_category="CREDENTIAL_THEFT",
            title="Credential Phishing",
            description="Phishing app exfiltrating user credentials",
        )
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_score >= 20.0
