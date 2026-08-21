"""Unit tests for Execution Path Analysis (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import ExecutionPathDTO


def test_execution_path_dto():
    path = ExecutionPathDTO(method_name="com.bank.IO.read", path_length=5, branch_count=2, exit_type="RETURN")

    assert path.method_name == "com.bank.IO.read"
    assert path.path_length == 5
    assert path.branch_count == 2
    assert path.exit_type == "RETURN"
