"""Unit Tests — Contradiction Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import ContradictionNarrativeGenerator


class TestContradictionNarrativeGenerator:
    """Mandatory Test Case 9: Contradiction Narrative generates unresolved conflict explanations."""

    def setup_method(self):
        self.gen = ContradictionNarrativeGenerator()

    def test_contradiction_narrative(self):
        c = SimpleNamespace(evidence_a="Evidence A", evidence_b="Evidence B")
        narrs = self.gen.generate([c])
        assert len(narrs) == 1
        assert "conflicting" in narrs[0].narrative.lower()
        assert narrs[0].resolution_status == "UNRESOLVED"

    def test_multiple_contradictions(self):
        contradictions = [SimpleNamespace(evidence_a=f"EA{i}", evidence_b=f"EB{i}") for i in range(3)]
        narrs = self.gen.generate(contradictions)
        assert len(narrs) == 3

    def test_empty_input(self):
        narrs = self.gen.generate([])
        assert narrs == []
