"""Unit tests for False Negative Prevention Suite (Phase 3.9 Part 1C)."""

import pytest
from app.services.risk_aggregation_engine import RiskAggregationEngine
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO


def test_false_negative_detection():
    engine = RiskAggregationEngine()
    findings = [
        CanonicalFindingDTO(
            finding_id="f_phish",
            finding_type="CREDENTIAL_PHISHING_EXFILTRATION",
            finding_category="CREDENTIAL_THEFT",
            title="Credential Phishing Exfiltration",
            description="Phishing form exfiltrating user passwords to known C2 server",
        )
    ]

    ass, factors, cat_scores, contribs, intr, mit, prot, cfl = engine.calculate_risk(findings)

    assert ass.risk_score >= 20.0
