"""Unit tests for Intra-Method Control Flow Graph Builder (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import CFGNodeDTO, CFGEdgeDTO


def test_cfg_node_and_edge_dtos():
    node1 = CFGNodeDTO(method_name="com.bank.Auth.login", block_id=1, start_offset=0, end_offset=12, is_entry=True)
    node2 = CFGNodeDTO(method_name="com.bank.Auth.login", block_id=2, start_offset=12, end_offset=24, is_exit=True)

    edge = CFGEdgeDTO(method_name="com.bank.Auth.login", source_block_id=1, target_block_id=2, edge_type="CONDITIONAL")

    assert node1.block_id == 1
    assert node1.is_entry is True
    assert node2.is_exit is True
    assert edge.source_block_id == 1
    assert edge.target_block_id == 2
    assert edge.edge_type == "CONDITIONAL"
