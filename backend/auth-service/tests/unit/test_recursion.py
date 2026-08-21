"""Unit tests for Tarjan SCC & Repository Persistence (Phase 3.7 Part 1A.15)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.program_graph_repository import ProgramGraphRepository
from app.schemas.program_graph_models import (
    ProgramGraphResultDTO,
    SCCNodeDTO,
    ProgramGraphMetricsDTO,
)


@pytest.mark.asyncio
async def test_program_graph_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = ProgramGraphRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = ProgramGraphResultDTO(
        sccs=[SCCNodeDTO(scc_id=1, node_count=4, is_recursive=True)],
        metrics=ProgramGraphMetricsDTO(cfg_count=10),
    )

    stats_model = await repo.save_full_program_graph(scan_id, dto)
    assert stats_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
