"""Unit tests for Report Validator Service (Phase 4.0 Part 1)."""

import pytest
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.services.report_validator import ReportValidator
from app.schemas.risk_aggregation_models import RiskAssessmentDTO


def test_report_validator_success():
    generator = DigitalTrustReportGenerator()
    validator = ReportValidator()

    risk_ass = RiskAssessmentDTO(
        assessment_id="a1",
        risk_score=25.0,
        risk_band="LOW_RISK",
        confidence_level="HIGH",
        evidence_sufficiency="SUFFICIENT",
    )

    doc = generator.build_report_document(analysis_id="an_1", risk_assessment_dto=risk_ass)
    res = validator.validate_report(doc, risk_ass)

    assert res is True
