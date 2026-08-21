"""Unit tests for Dominator Tree Construction (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import DominatorNodeDTO


def test_dominator_node_dto():
    dom = DominatorNodeDTO(method_name="com.bank.UI.draw", block_id=3, idom_block_id=1, depth=2)

    assert dom.method_name == "com.bank.UI.draw"
    assert dom.block_id == 3
    assert dom.idom_block_id == 1
    assert dom.depth == 2
