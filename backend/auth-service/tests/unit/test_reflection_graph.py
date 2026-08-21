"""Unit tests for Reflection Call Graph (Phase 3.7 Part 1A.17)."""

import pytest
from app.schemas.reflection_models import ReflectionGraphEdgeDTO


def test_reflection_graph_edge_dto():
    edge = ReflectionGraphEdgeDTO(caller_method="com.bank.Main.start", target_symbol="com.bank.Plugin.run", invocation_type="REFLECTIVE_INVOKE")

    assert edge.caller_method == "com.bank.Main.start"
    assert edge.target_symbol == "com.bank.Plugin.run"
    assert edge.invocation_type == "REFLECTIVE_INVOKE"
