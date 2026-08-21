"""Unit Tests — Mitigation & Protective Control Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import MitigationNarrativeGenerator


class TestMitigationNarrativeGenerator:
    """Mandatory Test Case 10: Mitigation Narrative generates protective control explanations."""

    def setup_method(self):
        self.gen = MitigationNarrativeGenerator()

    def test_mitigation_narrative(self):
        m = SimpleNamespace(name="Certificate Pinning")
        stmts = self.gen.generate([m])
        assert len(stmts) == 1
        assert "protective control" in stmts[0].claim.lower()
        assert "does not eliminate" in stmts[0].claim.lower()

    def test_string_mitigation(self):
        stmts = self.gen.generate(["ProGuard obfuscation"])
        assert len(stmts) == 1
        assert "ProGuard obfuscation" in stmts[0].claim

    def test_empty_input(self):
        stmts = self.gen.generate([])
        assert stmts == []
