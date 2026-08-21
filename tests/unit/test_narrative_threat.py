"""Unit Tests — Threat Intel Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import ThreatIntelNarrativeGenerator


class TestThreatIntelNarrativeGenerator:
    """Mandatory Test Case 8: Threat Intel Narrative for current and stale matches."""

    def setup_method(self):
        self.gen = ThreatIntelNarrativeGenerator()

    def test_current_match(self):
        match = SimpleNamespace(indicator="domain", freshness="CURRENT")
        stmts = self.gen.generate([match])
        assert len(stmts) == 1
        assert "currently classified as malicious" in stmts[0].claim.lower()
        assert stmts[0].claim_strength == "STRONGLY_SUPPORTED"

    def test_stale_match(self):
        match = SimpleNamespace(indicator="IP", freshness="STALE")
        stmts = self.gen.generate([match])
        assert len(stmts) == 1
        assert "stale" in stmts[0].claim.lower()
        assert stmts[0].claim_strength == "PARTIALLY_SUPPORTED"

    def test_empty_input(self):
        stmts = self.gen.generate([])
        assert stmts == []
