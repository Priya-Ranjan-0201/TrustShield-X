"""Unit tests for Graph Node & Edge Deduplication (Phase 3.9 Part 1A.25)."""

import pytest
from app.services.evidence_consolidation_orchestrator import EvidenceConsolidationOrchestrator


def test_orchestrator_graph_exporters():
    orchestrator = EvidenceConsolidationOrchestrator()
    res = orchestrator.run_consolidation()

    assert "digraph" in res.dot_export
    assert "graph TD" in res.mermaid_export
    assert "graphml" in res.graphml_export
