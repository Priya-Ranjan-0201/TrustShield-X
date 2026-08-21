"""Unit tests for Multi-Module Report Consolidation (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator


def test_report_module_integration():
    generator = DigitalTrustReportGenerator()
    modules = {"apk": "COMPLETED", "network": "COMPLETED", "audio": "COMPLETED"}
    doc = generator.build_report_document(analysis_id="an_1", module_results=modules)

    assert doc.module_results["audio"] == "COMPLETED"
