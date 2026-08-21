"""Unit tests for Async APK Binary Inventory Repository (Phase 3.7 Part 1A.12)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.apk_binary_inventory_repository import APKBinaryInventoryRepository
from app.schemas.apk_binary_inventory_models import (
    APKBinaryInventoryResultDTO,
    BinaryFileEntryDTO,
    BinaryHashDTO,
    BinaryStatisticsDTO,
    FileCategoryEnum,
)


@pytest.mark.asyncio
async def test_binary_inventory_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = APKBinaryInventoryRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = APKBinaryInventoryResultDTO(
        entries=[
            BinaryFileEntryDTO(
                file_path="classes.dex",
                filename="classes.dex",
                directory="",
                extension=".dex",
                file_category=FileCategoryEnum.DEX,
                uncompressed_size=1024,
                compressed_size=512,
                hashes=BinaryHashDTO(
                    sha256="a" * 64,
                    sha1="b" * 40,
                    md5="c" * 32,
                    crc32="00000000",
                    entropy=4.5,
                ),
            )
        ],
        statistics=BinaryStatisticsDTO(total_files=1, dex_count=1),
    )

    models = await repo.save_full_binary_inventory(scan_id, dto)
    assert len(models) == 1
    assert models[0].scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
