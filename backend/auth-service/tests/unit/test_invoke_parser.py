"""Unit tests for Method Metrics & Repository Persistence (Phase 3.7 Part 1A.14)."""

import uuid
import pytest
from unittest.mock import AsyncMock
from app.repositories.dex_instruction_repository import DEXInstructionRepository
from app.schemas.dex_instruction_models import (
    DEXInstructionResultDTO,
    DalvikInstructionDTO,
    OpcodeCategoryEnum,
    OpcodeStatisticsDTO,
)


@pytest.mark.asyncio
async def test_dex_instruction_repository_save_and_retrieve():
    db_mock = AsyncMock()
    repo = DEXInstructionRepository(db_mock)
    scan_id = uuid.uuid4()

    dto = DEXInstructionResultDTO(
        instructions=[
            DalvikInstructionDTO(
                class_name="com.bank.Net",
                method_name="connect",
                opcode_name="invoke-direct",
                opcode_val=0x70,
                offset=0,
                category=OpcodeCategoryEnum.INVOKE,
            )
        ],
        statistics=OpcodeStatisticsDTO(total_instructions=1),
    )

    stats_model = await repo.save_full_instruction_intelligence(scan_id, dto)
    assert stats_model.scan_id == scan_id
    assert db_mock.add.called
    assert db_mock.commit.called
