"""Unit tests for Async Intent Repository (Phase 3.7 Part 1A.10)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.intent_repository import IntentRepository
from app.schemas.intent_intelligence_models import (
    IntentIntelligenceResultDTO,
    EnrichedDeepLinkDTO,
    NavigationNodeDTO,
    IntentStatisticsDTO,
)


@pytest.mark.asyncio
async def test_intent_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = IntentRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = IntentIntelligenceResultDTO(
        deep_links=[
            EnrichedDeepLinkDTO(
                component_name=".MainActivity",
                scheme="https",
                host="example.com",
                is_app_link=True,
                is_browsable=True,
            )
        ],
        navigation_nodes=[
            NavigationNodeDTO(
                source_component="EXTERNAL_INTENT",
                intent_action="android.intent.action.VIEW",
                target_scheme="https",
                target_host="example.com",
                destination_component=".MainActivity",
            )
        ],
        statistics=IntentStatisticsDTO(total_deep_links=1),
    )

    models = await repo.save_full_intent_intelligence(scan_id, dto)
    assert len(models) == 1
    assert models[0].scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
