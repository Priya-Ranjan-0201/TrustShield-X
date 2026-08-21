"""Unit tests for Opcode Parsing & DTO Contracts (Phase 3.7 Part 1A.14)."""

import pytest
from app.schemas.dex_instruction_models import DalvikInstructionDTO, OpcodeCategoryEnum


def test_dalvik_instruction_dto():
    inst = DalvikInstructionDTO(
        class_name="com.bank.auth.LoginManager",
        method_name="performLogin",
        opcode_name="invoke-virtual",
        opcode_val=0x6E,
        offset=0x0012,
        length=3,
        category=OpcodeCategoryEnum.INVOKE,
    )

    assert inst.class_name == "com.bank.auth.LoginManager"
    assert inst.method_name == "performLogin"
    assert inst.opcode_name == "invoke-virtual"
    assert inst.opcode_val == 110
    assert inst.offset == 18
    assert inst.category == OpcodeCategoryEnum.INVOKE
