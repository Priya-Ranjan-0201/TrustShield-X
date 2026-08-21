"""Unit tests for Report Generation Service (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator


def test_report_generation_service():
    generator = DigitalTrustReportGenerator()
    doc = generator.build_report_document(analysis_id="an_test")

    assert doc.analysis_id == "an_test"
    assert doc.trust_overview.risk_score == 0.0
    assert doc.trust_overview.risk_band == "TRUSTED"
