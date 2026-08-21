"""Unit tests for Instruction Operand Extraction (Phase 3.7 Part 1A.14)."""

import pytest
from app.schemas.dex_instruction_models import InstructionOperandDTO


def test_instruction_operand_dto():
    op1 = InstructionOperandDTO(operand_type="REGISTER", operand_value="v0")
    op2 = InstructionOperandDTO(operand_type="STRING_REF", operand_value="https://api.bank.com")

    assert op1.operand_type == "REGISTER"
    assert op1.operand_value == "v0"
    assert op2.operand_type == "STRING_REF"
    assert op2.operand_value == "https://api.bank.com"
