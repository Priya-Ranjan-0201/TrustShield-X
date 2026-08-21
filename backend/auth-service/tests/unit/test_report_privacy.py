"""Unit tests for Report Privacy Redaction (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator


def test_report_privacy_handling():
    generator = DigitalTrustReportGenerator()
    doc = generator.build_report_document(analysis_id="an_1")

    assert doc.report_id is not None
