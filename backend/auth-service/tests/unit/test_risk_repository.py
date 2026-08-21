"""Unit tests for Risk Repository Persistence (Phase 3.9 Part 1B)."""

import pytest
import uuid
from unittest.mock import AsyncMock
from app.repositories.risk_repository import RiskRepository
from app.schemas.risk_aggregation_models import RiskAssessmentResultDTO, RiskAssessmentDTO, RiskAuditRecordDTO, RiskPolicyVersionDTO, RiskDecisionRecordDTO, RiskMetricsDTO, RiskExplanationDTO, RiskSummaryDTO


@pytest.mark.asyncio
async def test_risk_repository_save():
    mock_db = AsyncMock()
    repo = RiskRepository(mock_db)

    ass = RiskAssessmentDTO(assessment_id="ass_1")
    aud = RiskAuditRecordDTO(audit_id="aud_1", audit_trail_text="Text")
    ver = RiskPolicyVersionDTO()
    dec = RiskDecisionRecordDTO(decision_id="dec_1")
    m = RiskMetricsDTO()
    exp = RiskExplanationDTO(explanation_id="exp_1", summary_text="Text")
    sum_dto = RiskSummaryDTO(title="Title")

    dto = RiskAssessmentResultDTO(
        assessment=ass,
        audit_record=aud,
        policy_version=ver,
        decision_record=dec,
        metrics=m,
        explanation=exp,
        summary=sum_dto,
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_risk_assessment(scan_id, dto)

    assert model.assessment_id == "ass_1"
    assert mock_db.commit.called
