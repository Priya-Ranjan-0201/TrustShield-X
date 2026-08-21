"""Unit tests for Threat Intelligence Repository Persistence (Phase 3.9 Part 1A.23)."""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.repositories.threat_intelligence_repository import ThreatIntelligenceRepository
from app.schemas.threat_intelligence_models import ThreatIntelligenceResultDTO, ThreatIndicatorDTO


@pytest.mark.asyncio
async def test_threat_repository_save():
    mock_db = AsyncMock()
    repo = ThreatIntelligenceRepository(mock_db)

    dto = ThreatIntelligenceResultDTO(
        indicators=[
            ThreatIndicatorDTO(
                indicator_id="ind_1",
                indicator_type="DOMAIN",
                normalized_value="example.com",
                display_value="example.com",
                value_hash="hash_1",
                source_module="NET",
                source_location="net",
            )
        ]
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_threat_intelligence(scan_id, dto)

    assert model.indicator_id == "ind_1"
    assert mock_db.commit.called
