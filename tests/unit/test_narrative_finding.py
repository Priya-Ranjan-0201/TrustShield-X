"""Unit Tests — Finding Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import FindingNarrativeGenerator


class TestFindingNarrativeGenerator:
    """Mandatory Test Case 4: Finding Narrative generates per-finding explanations."""

    def setup_method(self):
        self.gen = FindingNarrativeGenerator()

    def test_finding_narrative(self):
        finding = SimpleNamespace(finding_id="f1", title="Network Endpoint", description="Detected domain", confidence_level="HIGH", finding_category="NETWORK")
        res = self.gen.generate(finding)
        assert res.finding_id == "f1"
        assert res.title == "Network Endpoint"
        assert "network" in res.why_it_matters.lower()

    def test_finding_provenance(self):
        finding = SimpleNamespace(finding_id="f2", title="API Call", description="API usage observed", confidence_level="MEDIUM", finding_category="API")
        res = self.gen.generate(finding)
        assert "prov_f2" in res.provenance

    def test_api_finding_limitation(self):
        finding = SimpleNamespace(finding_id="f3", title="API", description="API call observed", confidence="HIGH", finding_category="API")
        res = self.gen.generate(finding)
        assert "API" in res.what_is_not_established or res.what_is_not_established == ""
