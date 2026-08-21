"""Unit tests for Behavior Rule Repository Persistence (Phase 3.9 Part 1A.24)."""

import pytest
import uuid
from unittest.mock import AsyncMock
from app.repositories.behavior_rule_repository import BehaviorRuleRepository
from app.schemas.behavior_rule_models import RuleResultDTO, BehaviorRuleEvaluationDTO


@pytest.mark.asyncio
async def test_rule_repository_save():
    mock_db = AsyncMock()
    repo = BehaviorRuleRepository(mock_db)

    dto = RuleResultDTO(
        evaluations=[
            BehaviorRuleEvaluationDTO(
                evaluation_id="eval_1",
                rule_id="RULE-DATAFLOW-001",
                rule_version="1.0.0",
                namespace="DATAFLOW",
                state="MATCHED",
                confidence="HIGH",
                evidence_provenance="SMS Dataflow Path",
            )
        ]
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_rule_result(scan_id, dto)

    assert model.rule_id == "RULE-DATAFLOW-001"
    assert mock_db.commit.called
