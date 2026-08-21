"""Unit tests for Multi-DEX Cryptography Resolution & Repository Persistence (Phase 3.7 Part 1A.18)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.cryptography_repository import CryptographyRepository
from app.schemas.cryptography_models import (
    CryptographyResultDTO,
    CryptoAlgorithmDTO,
    CryptoMetricsDTO,
)


@pytest.mark.asyncio
async def test_cryptography_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = CryptographyRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = CryptographyResultDTO(
        algorithms=[
            CryptoAlgorithmDTO(
                algorithm_name="AES-256-GCM",
                family="SYMMETRIC",
                key_size=256,
            )
        ],
        metrics=CryptoMetricsDTO(algorithms_count=1),
    )

    first_model = await repo.save_full_cryptography_intelligence(scan_id, dto)
    assert first_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
