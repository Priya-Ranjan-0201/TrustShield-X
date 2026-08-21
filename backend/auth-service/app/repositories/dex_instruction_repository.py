"""Async DEX Instruction Repository Layer (Phase 3.7 Part 1A.14).

Provides database operations for persisting and retrieving dex_instructions,
dex_operands, dex_basic_blocks, dex_control_flow, and dex_opcode_statistics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dex_instruction import (
    DEXInstructionModel,
    DEXOperandModel,
    DEXBasicBlockModel,
    DEXControlFlowModel,
    DEXOpcodeStatisticsModel,
)
from app.schemas.dex_instruction_models import DEXInstructionResultDTO


class DEXInstructionRepository:
    """Async repository for DEX Instruction DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_instruction_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: DEXInstructionResultDTO,
    ) -> DEXOpcodeStatisticsModel:
        """Saves instructions, operands, basic blocks, control flow edges, and statistics inside one atomic transaction."""
        for inst in dto.instructions:
            inst_m = DEXInstructionModel(
                scan_id=scan_id,
                class_name=inst.class_name,
                method_name=inst.method_name,
                opcode_name=inst.opcode_name,
                opcode_val=inst.opcode_val,
                offset=inst.offset,
                length=inst.length,
                category=inst.category.value if hasattr(inst.category, 'value') else str(inst.category),
            )
            self.db.add(inst_m)
            await self.db.flush()

            for op in inst.operands:
                op_m = DEXOperandModel(
                    instruction_id=inst_m.id,
                    operand_type=op.operand_type,
                    operand_val=op.operand_value,
                )
                self.db.add(op_m)

        for bb in dto.basic_blocks:
            self.db.add(
                DEXBasicBlockModel(
                    scan_id=scan_id,
                    method_name=bb.method_name,
                    start_offset=bb.start_offset,
                    end_offset=bb.end_offset,
                    instruction_count=bb.instruction_count,
                )
            )

        for edge in dto.control_flow:
            self.db.add(
                DEXControlFlowModel(
                    scan_id=scan_id,
                    source_offset=edge.source_offset,
                    target_offset=edge.target_offset,
                    branch_type=edge.branch_type,
                )
            )

        stats_m = DEXOpcodeStatisticsModel(
            scan_id=scan_id,
            total_instructions=dto.statistics.total_instructions,
            unique_opcodes=dto.statistics.unique_opcodes,
            most_common_opcode=dto.statistics.most_common_opcode,
            avg_instructions_per_method=dto.statistics.avg_instructions_per_method,
        )
        self.db.add(stats_m)

        await self.db.commit()
        return stats_m

    async def get_instructions(self, scan_id: uuid.UUID) -> List[DEXInstructionModel]:
        stmt = (
            select(DEXInstructionModel)
            .where(DEXInstructionModel.scan_id == scan_id)
            .options(selectinload(DEXInstructionModel.operands))
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
