"""Unit tests for Report Failure Graceful Handling (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator


def test_report_failure_recovery_empty():
    generator = DigitalTrustReportGenerator()
    doc = generator.build_report_document(analysis_id="an_empty")

    assert doc.status == "COMPLETED"
    assert doc.trust_overview.risk_score == 0.0
