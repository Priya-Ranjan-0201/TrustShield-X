"""Unit tests for Dataflow Repository Persistence (Phase 3.9 Part 1A.21)."""

import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock
from app.repositories.dataflow_repository import DataflowRepository
from app.schemas.dataflow_models import DataflowResultDTO, DataflowNodeDTO


@pytest.mark.asyncio
async def test_dataflow_repository_save():
    mock_db = AsyncMock()
    repo = DataflowRepository(mock_db)

    dto = DataflowResultDTO(
        nodes=[
            DataflowNodeDTO(
                node_id="src_1",
                node_type="SOURCE",
                label="Location Source",
                class_name="com.bank.LocationClient",
                method_name="getLocation",
            )
        ]
    )

    scan_id = uuid.uuid4()
    model = await repo.save_full_dataflow_intelligence(scan_id, dto)

    assert model.node_id == "src_1"
    assert mock_db.commit.called
