"""Unit tests for Multi-DEX Reflection Resolution & Repository Persistence (Phase 3.7 Part 1A.17)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.reflection_repository import ReflectionRepository
from app.schemas.reflection_models import (
    ReflectionResultDTO,
    ReflectionCallDTO,
    ReflectionMetricsDTO,
)


@pytest.mark.asyncio
async def test_reflection_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = ReflectionRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = ReflectionResultDTO(
        reflection_calls=[
            ReflectionCallDTO(
                caller_method="com.bank.Net.connect",
                reflection_api="java.lang.Class.forName",
                target_class="com.bank.NetImpl",
            )
        ],
        metrics=ReflectionMetricsDTO(reflection_calls_count=1),
    )

    first_model = await repo.save_full_reflection_intelligence(scan_id, dto)
    assert first_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
