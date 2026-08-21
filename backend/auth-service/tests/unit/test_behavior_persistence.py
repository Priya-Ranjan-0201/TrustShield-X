"""Unit tests for Behavioral Correlation Repository Persistence (Phase 3.9 Part 1A.22)."""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.repositories.behavioral_correlation_repository import BehavioralCorrelationRepository
from app.schemas.behavioral_correlation_models import BehavioralCorrelationResultDTO, BehaviorFindingDTO


@pytest.mark.asyncio
async def test_behavior_repository_save():
    mock_db = AsyncMock()
    repo = BehavioralCorrelationRepository(mock_db)

    dto = BehavioralCorrelationResultDTO(
        findings=[
            BehaviorFindingDTO(
                finding_id="f_1",
                finding_type="SMS_DATA_NETWORK_FLOW",
                category="SMS_DATA_FLOW",
                evidence_strength="DIRECT",
                summary="SMS flow test",
            )
        ]
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_behavioral_correlation(scan_id, dto)

    assert model.finding_id == "f_1"
    assert mock_db.commit.called
