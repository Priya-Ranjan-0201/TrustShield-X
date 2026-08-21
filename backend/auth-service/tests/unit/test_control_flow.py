"""Unit tests for Basic Blocks and Control Flow Edges (Phase 3.7 Part 1A.14)."""

import pytest
from app.schemas.dex_instruction_models import BasicBlockDTO, ControlFlowEdgeDTO


def test_basic_block_dto():
    bb = BasicBlockDTO(
        method_name="com.bank.Crypto.encrypt",
        start_offset=0,
        end_offset=24,
        instruction_count=8,
    )
    assert bb.method_name == "com.bank.Crypto.encrypt"
    assert bb.instruction_count == 8


def test_control_flow_edge_dto():
    edge = ControlFlowEdgeDTO(
        source_offset=12,
        target_offset=34,
        branch_type="JUMP",
    )
    assert edge.source_offset == 12
    assert edge.target_offset == 34
    assert edge.branch_type == "JUMP"
