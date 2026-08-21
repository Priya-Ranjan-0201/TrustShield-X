"""Unit tests for File Dataflow (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowEdgeDTO


def test_file_edge_dto():
    edge = DataflowEdgeDTO(
        source_node_id="data_buf",
        target_node_id="file_target",
        edge_type="FILE_WRITE",
        caller_method="com.bank.FileIO.write",
    )

    assert edge.edge_type == "FILE_WRITE"
