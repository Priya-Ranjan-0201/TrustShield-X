"""Unit tests for API Schema Contract Integrity (Phase 3.9 Part 1C)."""

import pytest
from app.schemas.envelope import ResponseEnvelope
from app.schemas.risk_aggregation_models import RiskAssessmentDTO


def test_api_contract_response_envelope():
    dto = RiskAssessmentDTO(assessment_id="test_contract")
    env = ResponseEnvelope(message="Success", data=dto)

    assert env.success is True
    assert env.data.assessment_id == "test_contract"
