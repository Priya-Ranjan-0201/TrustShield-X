"""Unit tests for Report Generation Idempotency (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_orchestrator import DigitalTrustReportOrchestrator


def test_report_generation_idempotency():
    orchestrator = DigitalTrustReportOrchestrator()
    r1 = orchestrator.generate_report(analysis_id="an_idem")
    r2 = orchestrator.generate_report(analysis_id="an_idem")

    assert r1.document.trust_overview.risk_score == r2.document.trust_overview.risk_score
    assert r1.document.trust_overview.risk_band == r2.document.trust_overview.risk_band
