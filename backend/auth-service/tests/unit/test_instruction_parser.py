"""Unit tests for DEX Instruction Intelligence Parser (Phase 3.7 Part 1A.14)."""

import pytest
from app.services.dex_instruction_service import DEXInstructionService
from app.schemas.dex_instruction_models import OpcodeCategoryEnum


def test_categorize_opcodes():
    service = DEXInstructionService()

    assert service.categorize_opcode("invoke-virtual") == OpcodeCategoryEnum.INVOKE
    assert service.categorize_opcode("invoke-static") == OpcodeCategoryEnum.INVOKE
    assert service.categorize_opcode("iget-object") == OpcodeCategoryEnum.FIELD_ACCESS
    assert service.categorize_opcode("sput-boolean") == OpcodeCategoryEnum.FIELD_ACCESS
    assert service.categorize_opcode("return-void") == OpcodeCategoryEnum.RETURN
    assert service.categorize_opcode("const-string") == OpcodeCategoryEnum.CONSTANT
    assert service.categorize_opcode("goto/16") == OpcodeCategoryEnum.GOTO
    assert service.categorize_opcode("if-eqz") == OpcodeCategoryEnum.IF
    assert service.categorize_opcode("new-instance") == OpcodeCategoryEnum.NEW_INSTANCE
    assert service.categorize_opcode("throw") == OpcodeCategoryEnum.THROW
