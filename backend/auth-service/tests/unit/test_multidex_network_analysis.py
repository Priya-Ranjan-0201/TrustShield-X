"""Unit tests for Multi-DEX Network Analysis & Repository Persistence (Phase 3.8 Part 1A.19)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.network_repository import NetworkRepository
from app.schemas.network_models import (
    NetworkIntelligenceResultDTO,
    NetworkEndpointDTO,
    NetworkMetricsDTO,
)


@pytest.mark.asyncio
async def test_network_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = NetworkRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = NetworkIntelligenceResultDTO(
        endpoints=[
            NetworkEndpointDTO(
                url="https://api.bank.com/v1/data",
                scheme="https",
                host="api.bank.com",
                source_class="com.bank.MultiDexNet",
                source_method="com.bank.MultiDexNet.connect",
            )
        ],
        metrics=NetworkMetricsDTO(endpoints_count=1),
    )

    first_model = await repo.save_full_network_intelligence(scan_id, dto)
    assert first_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
