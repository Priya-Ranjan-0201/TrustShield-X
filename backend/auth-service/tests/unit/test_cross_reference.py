"""Unit tests for Bidirectional Cross-References (Phase 3.7 Part 1A.15)."""

import pytest
from app.schemas.program_graph_models import MethodXRefDTO


def test_method_xref_dto():
    xref = MethodXRefDTO(source_symbol="com.bank.Main.start", target_symbol="com.bank.Net.connect", xref_type="CALL")

    assert xref.source_symbol == "com.bank.Main.start"
    assert xref.target_symbol == "com.bank.Net.connect"
    assert xref.xref_type == "CALL"
