"""Unit tests for Dataflow Frontend Dashboard Contract (Phase 3.9 Part 1A.21)."""

import pytest
from app.schemas.dataflow_models import DataflowPathDTO, DataflowMetricsDTO


def test_dataflow_frontend_contract():
    path = DataflowPathDTO(
        path_id="path_src_1_snk_1",
        source_id="src_location",
        sink_id="snk_http",
        path_nodes=["LocationManager.getLastKnownLocation", "JSONSerializer", "OkHttpClient.post"],
        flow_classification="SOURCE_TO_NETWORK",
        confidence="HIGH",
        resolution_status="RESOLVED",
    )
    metrics = DataflowMetricsDTO(
        methods_analyzed=120,
        instructions_analyzed=1440,
        sources_count=2,
        sinks_count=2,
        paths_count=2,
        taint_labels_count=2,
        unresolved_boundaries_count=0,
    )

    assert path.path_id == "path_src_1_snk_1"
    assert metrics.paths_count == 2
