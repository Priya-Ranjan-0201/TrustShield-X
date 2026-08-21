"""Unit tests for Async Permission Repository (Phase 3.7 Part 1A.8)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission_intelligence_models import (
    PermissionIntelligenceResultDTO,
    EnrichedPermissionDTO,
    PermissionStatisticsDTO,
)


@pytest.mark.asyncio
async def test_permission_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = PermissionRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = PermissionIntelligenceResultDTO(
        permissions=[
            EnrichedPermissionDTO(
                permission_name="android.permission.CAMERA",
                category="Camera",
                protection_level="DANGEROUS",
                is_runtime=True,
                is_dangerous=True,
            )
        ],
        statistics=PermissionStatisticsDTO(total_permissions=1, dangerous_count=1),
    )

    models = await repo.save_full_permission_intelligence(scan_id, dto)
    assert len(models) == 1
    assert models[0].scan_id == scan_id
    assert db_mock.add_all.called
    assert db_mock.commit.called
