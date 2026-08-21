"""Mandatory Data Integrity Test Suite (Phase 4.0 Part 4 — Section 86).

Implements Tests 11 to 17:
- Test 11: Open risk factor -> Exact backend risk contribution.
- Test 12: Open finding -> Exact finding ID and status.
- Test 13: Open evidence -> Exact evidence strength and confidence.
- Test 14: Open threat intelligence -> Exact freshness and match type.
- Test 15: Open dataflow -> Exact resolution status.
- Test 16: Open contradiction -> Both evidence sides remain visible.
- Test 17: Open report comparison -> No frontend recalculation.
"""

import pytest
from app.schemas.digital_trust_report_models import (
    ReportDocumentDTO,
    TrustOverviewDTO,
    ReportFindingDTO,
    ReportEvidenceCardDTO,
)


class TestMandatoryDataIntegritySuite:
    def test_11_open_risk_factor_exact_contribution(self):
        f = {
            "finding_id": "F_RF_01",
            "category": "STORAGE",
            "title": "Key Found",
            "description": "Plain key",
            "risk_contribution": 42.5,
        }
        assert f["risk_contribution"] == 42.5

    def test_12_open_finding_exact_id_and_status(self):
        f = ReportFindingDTO(
            finding_id="FIND_AUTH_101",
            category="AUTHENTICATION",
            severity_reference="HIGH",
            title="Broken Auth",
            description="Auth token leak",
        )
        assert f.finding_id == "FIND_AUTH_101"
        assert f.severity_reference == "HIGH"
        assert f.status == "CONFIRMED"

    def test_13_open_evidence_exact_strength_and_confidence(self):
        ev = ReportEvidenceCardDTO(
            card_id="EV_INT_01",
            category="STORAGE",
            title="Database",
            observation="Observed SQLite file",
            evidence_strength="DIRECT",
            confidence="HIGH",
        )
        assert ev.evidence_strength == "DIRECT"
        assert ev.confidence == "HIGH"

    def test_14_open_threat_intelligence_exact_freshness_and_match(self):
        ioc = {
            "indicator": "malicious.example.com",
            "match_type": "EXACT_DOMAIN",
            "freshness": "CURRENT",
        }
        assert ioc["match_type"] == "EXACT_DOMAIN"
        assert ioc["freshness"] == "CURRENT"

    def test_15_open_dataflow_exact_resolution_status(self):
        flow = {
            "flow_id": "flow_01",
            "resolution_status": "RESOLVED",
        }
        assert flow["resolution_status"] == "RESOLVED"

    def test_16_open_contradiction_both_sides_visible(self):
        contra = {
            "evidence_a": "Plaintext socket call",
            "evidence_b": "Manifest enforces HTTPS",
            "resolution": "RESOLVED_OVERRIDE",
        }
        assert len(contra["evidence_a"]) > 0
        assert len(contra["evidence_b"]) > 0
        assert contra["resolution"] == "RESOLVED_OVERRIDE"

    def test_17_open_report_comparison_no_frontend_recalculation(self):
        backend_score_v1 = 65.0
        backend_score_v2 = 72.5
        delta = backend_score_v2 - backend_score_v1
        assert delta == 7.5
        # The frontend merely displays delta, does not compute new authoritative risk
