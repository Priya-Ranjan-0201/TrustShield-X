"""Unit tests for Report Risk Score Mismatch Enforcement (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.services.report_validator import ReportValidator
from app.schemas.risk_aggregation_models import RiskAssessmentDTO


def test_report_risk_mismatch_error():
    generator = DigitalTrustReportGenerator()
    validator = ReportValidator()

    doc = generator.build_report_document(analysis_id="an_1")

    # Mismatched risk assessment
    mismatched_ass = RiskAssessmentDTO(
        assessment_id="a1",
        risk_score=95.0,  # Mismatch against doc score (0.0)
        risk_band="CRITICAL_RISK",
        confidence_level="HIGH",
        evidence_sufficiency="SUFFICIENT",
    )

    with pytest.raises(ValueError, match="REPORT_GENERATION_ERROR"):
        validator.validate_report(doc, mismatched_ass)
