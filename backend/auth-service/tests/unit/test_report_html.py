"""Unit tests for Report HTML Rendering (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_orchestrator import DigitalTrustReportOrchestrator


def test_report_html_rendering():
    orchestrator = DigitalTrustReportOrchestrator()
    doc = orchestrator.generator.build_report_document(analysis_id="an_1")
    html = orchestrator.render_html_report(doc)

    assert "🛡️ Digital Trust Report" in html
    assert doc.report_id in html
