"""Unit Tests — Behavior Chain Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import BehaviorNarrativeGenerator


class TestBehaviorNarrativeGenerator:
    """Mandatory Test Case 7: Behavior Narrative generates chain explanations."""

    def setup_method(self):
        self.gen = BehaviorNarrativeGenerator()

    def test_behavior_chain(self):
        chain = SimpleNamespace(nodes=["READ_SMS", "ENCRYPT", "SEND_NETWORK"])
        stmts = self.gen.generate([chain])
        assert len(stmts) == 1
        assert "behavior chain" in stmts[0].claim.lower()
        assert stmts[0].claim_strength == "CORRELATED"

    def test_no_nodes(self):
        chain = SimpleNamespace(nodes=[])
        stmts = self.gen.generate([chain])
        assert len(stmts) == 1
        assert "behavioral correlation" in stmts[0].claim.lower()

    def test_empty_input(self):
        stmts = self.gen.generate([])
        assert stmts == []
