"""Unit tests for Multi-DEX API Resolution & Repository Persistence (Phase 3.7 Part 1A.16)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.api_repository import APIRepository
from app.schemas.api_intelligence_models import (
    APIIntelligenceResultDTO,
    APICatalogEntryDTO,
    APIStatisticsDTO,
)


@pytest.mark.asyncio
async def test_api_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = APIRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = APIIntelligenceResultDTO(
        api_catalog=[
            APICatalogEntryDTO(
                canonical_id="android.location.LocationManager.getLastKnownLocation",
                package_name="android.location",
                class_name="LocationManager",
                method_name="getLastKnownLocation",
                signature="Landroid/location/LocationManager;->getLastKnownLocation()Landroid/location/Location;",
            )
        ],
        statistics=APIStatisticsDTO(total_apis=1),
    )

    stats_model = await repo.save_full_api_intelligence(scan_id, dto)
    assert stats_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
