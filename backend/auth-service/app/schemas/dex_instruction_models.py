"""Pydantic v2 DTO Schemas for DEX Instruction & Opcode Intelligence Engine (Phase 3.7 Part 1A.14).

Strictly typed DTOs for Dalvik opcodes, instructions, operands, basic blocks,
control-flow edges, method metrics, and opcode statistics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class OpcodeCategoryEnum(str, Enum):
    MOVE = "MOVE"
    RETURN = "RETURN"
    CONSTANT = "CONSTANT"
    MONITOR = "MONITOR"
    CHECK_CAST = "CHECK_CAST"
    INSTANCE_OF = "INSTANCE_OF"
    ARRAY = "ARRAY"
    NEW_INSTANCE = "NEW_INSTANCE"
    THROW = "THROW"
    GOTO = "GOTO"
    SWITCH = "SWITCH"
    COMPARE = "COMPARE"
    IF = "IF"
    ARITHMETIC = "ARITHMETIC"
    LOGICAL = "LOGICAL"
    INVOKE = "INVOKE"
    FIELD_ACCESS = "FIELD_ACCESS"
    SYNCHRONIZATION = "SYNCHRONIZATION"
    EXCEPTION = "EXCEPTION"
    UNKNOWN = "UNKNOWN"


class InstructionOperandDTO(BaseModel):
    operand_type: str  # REGISTER, CONSTANT, METHOD_REF, FIELD_REF, STRING_REF, BRANCH_TARGET
    operand_value: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DalvikInstructionDTO(BaseModel):
    class_name: str
    method_name: str
    opcode_name: str
    opcode_val: int
    offset: int
    length: int = 2
    category: OpcodeCategoryEnum = OpcodeCategoryEnum.UNKNOWN
    operands: List[InstructionOperandDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class BasicBlockDTO(BaseModel):
    method_name: str
    start_offset: int
    end_offset: int
    instruction_count: int

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ControlFlowEdgeDTO(BaseModel):
    source_offset: int
    target_offset: int
    branch_type: str = "JUMP"  # JUMP, FALLTHROUGH, SWITCH, EXCEPTION

    model_config = ConfigDict(frozen=True, from_attributes=True)


class MethodInstructionMetricsDTO(BaseModel):
    method_name: str
    class_name: str
    instruction_count: int = 0
    branch_count: int = 0
    invoke_count: int = 0
    field_access_count: int = 0
    return_count: int = 0
    max_registers: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class OpcodeStatisticsDTO(BaseModel):
    total_instructions: int = 0
    unique_opcodes: int = 0
    most_common_opcode: Optional[str] = None
    avg_instructions_per_method: float = 0.0

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DEXInstructionResultDTO(BaseModel):
    instructions: List[DalvikInstructionDTO] = Field(default_factory=list)
    basic_blocks: List[BasicBlockDTO] = Field(default_factory=list)
    control_flow: List[ControlFlowEdgeDTO] = Field(default_factory=list)
    metrics: List[MethodInstructionMetricsDTO] = Field(default_factory=list)
    statistics: OpcodeStatisticsDTO = Field(default_factory=OpcodeStatisticsDTO)
    parsing_time_ms: int = 0

    model_config = ConfigDict(frozen=True, from_attributes=True)
