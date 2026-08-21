"""Unit tests for Async Component Repository (Phase 3.7 Part 1A.9)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.component_repository import ComponentRepository
from app.schemas.component_intelligence_models import (
    ComponentIntelligenceResultDTO,
    EnrichedComponentDTO,
    EnrichedIntentFilterDTO,
    ComponentStatisticsDTO,
    ExportStatus,
)


@pytest.mark.asyncio
async def test_component_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = ComponentRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = ComponentIntelligenceResultDTO(
        components=[
            EnrichedComponentDTO(
                name=".MainActivity",
                component_type="ACTIVITY",
                exported_status=ExportStatus.IMPLICIT_EXPORTED,
                is_launcher=True,
                intent_filters=[
                    EnrichedIntentFilterDTO(
                        actions=["android.intent.action.MAIN"],
                        categories=["android.intent.category.LAUNCHER"],
                        is_launcher=True,
                    )
                ],
            )
        ],
        statistics=ComponentStatisticsDTO(total_components=1, activities_count=1),
    )

    models = await repo.save_full_component_intelligence(scan_id, dto)
    assert len(models) == 1
    assert models[0].scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
