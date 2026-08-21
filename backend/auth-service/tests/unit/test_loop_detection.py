"""Unit tests for Natural Loop Detection (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import LoopAnalysisDTO


def test_loop_analysis_dto():
    loop = LoopAnalysisDTO(method_name="com.bank.Crypto.hashLoop", header_block_id=2, loop_depth=2)

    assert loop.method_name == "com.bank.Crypto.hashLoop"
    assert loop.header_block_id == 2
    assert loop.loop_depth == 2
