"""Unit tests for String Inventory & Repository Persistence (Phase 3.7 Part 1A.13)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.dex_structure_repository import DEXStructureRepository
from app.schemas.dex_structure_models import (
    DEXStructureResultDTO,
    StringEntryDTO,
    DEXStructureStatisticsDTO,
)


@pytest.mark.asyncio
async def test_dex_structure_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = DEXStructureRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = DEXStructureResultDTO(
        strings=[
            StringEntryDTO(
                string_value="https://api.bank.com/v1/auth",
                length=29,
                string_hash="a" * 64,
                offset=0x1000,
            )
        ],
        statistics=DEXStructureStatisticsDTO(total_strings=1),
    )

    stats_model = await repo.save_full_dex_structure(scan_id, dto)
    assert stats_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
