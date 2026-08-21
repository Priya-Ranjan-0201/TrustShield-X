"""Unit Tests — Dataflow Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import DataflowNarrativeGenerator


class TestDataflowNarrativeGenerator:
    """Mandatory Test Case 6: Dataflow Narrative for resolved and unresolved paths."""

    def setup_method(self):
        self.gen = DataflowNarrativeGenerator()

    def test_resolved_path(self):
        path = SimpleNamespace(path_id="p1", source="contacts", sink="https://api.example.com", resolution_status="RESOLVED")
        stmts = self.gen.generate([path])
        assert len(stmts) == 1
        assert "resolved" in stmts[0].claim.lower()
        assert stmts[0].claim_strength == "DIRECTLY_OBSERVED"

    def test_unresolved_path(self):
        path = SimpleNamespace(path_id="p2", source="sms", sink="unknown", resolution_status="UNRESOLVED")
        stmts = self.gen.generate([path])
        assert len(stmts) == 1
        assert "could not be resolved" in stmts[0].claim.lower()
        assert stmts[0].claim_strength == "PARTIALLY_SUPPORTED"

    def test_empty_input(self):
        stmts = self.gen.generate([])
        assert stmts == []
