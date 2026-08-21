"""Unit tests for Inter-Method Call Graph Construction (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import CallGraphNodeDTO, CallGraphEdgeDTO


def test_call_graph_nodes_and_edges():
    n1 = CallGraphNodeDTO(method_name="main", class_name="com.bank.Main", in_degree=0, out_degree=2)
    n2 = CallGraphNodeDTO(method_name="auth", class_name="com.bank.Auth", in_degree=1, out_degree=0)

    e1 = CallGraphEdgeDTO(caller_method="com.bank.Main.main", callee_method="com.bank.Auth.auth", invoke_type="INVOKE_STATIC")

    assert n1.in_degree == 0
    assert n1.out_degree == 2
    assert e1.caller_method == "com.bank.Main.main"
    assert e1.callee_method == "com.bank.Auth.auth"
    assert e1.invoke_type == "INVOKE_STATIC"
