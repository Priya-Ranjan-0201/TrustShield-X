"""Unit tests for Source-to-Sink Paths Engine (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowPathDTO, SourceSinkGraphDTO


def test_source_sink_path_dtos():
    path = DataflowPathDTO(
        path_id="path_1",
        source_id="src_loc",
        sink_id="snk_net",
        path_nodes=["src_loc", "trans_gson", "snk_net"],
        flow_classification="SOURCE_TO_NETWORK",
        confidence="HIGH",
    )
    ssg = SourceSinkGraphDTO(
        source_node="src_loc",
        sink_node="snk_net",
        path_length=2,
    )

    assert path.flow_classification == "SOURCE_TO_NETWORK"
    assert ssg.path_length == 2
