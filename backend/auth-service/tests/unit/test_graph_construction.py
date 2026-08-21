"""Unit tests for Evidence & Finding Graph Construction (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import EvidenceGraphDTO, FindingGraphDTO


def test_graph_dtos():
    eg = EvidenceGraphDTO(nodes_count=10, edges_count=15)
    fg = FindingGraphDTO(nodes_count=5, edges_count=8)

    assert eg.nodes_count == 10
    assert fg.edges_count == 8
