"""Unit Tests — Evidence Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import EvidenceNarrativeGenerator


class TestEvidenceNarrativeGenerator:
    """Mandatory Test Case 5: Evidence Narrative generates observation and limitations."""

    def setup_method(self):
        self.gen = EvidenceNarrativeGenerator()

    def test_evidence_narrative(self):
        ev = SimpleNamespace(evidence_id="e1", observation="Domain observed", evidence_strength="STRONG", source="NetworkEngine")
        res = self.gen.generate(ev)
        assert res.evidence_id == "e1"
        assert "Domain observed" in res.what_was_observed
        assert res.evidence_strength == "STRONG"

    def test_evidence_limitations(self):
        ev = SimpleNamespace(evidence_id="e2", observation="Obs", evidence_strength="MEDIUM", source="DEXEngine")
        res = self.gen.generate(ev)
        assert len(res.limitations) >= 1

    def test_evidence_source(self):
        ev = SimpleNamespace(evidence_id="e3", description="Test", evidence_strength="HIGH", source_module="ManifestEngine")
        res = self.gen.generate(ev)
        assert res.source == "ManifestEngine"
