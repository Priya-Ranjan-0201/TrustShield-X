"""Unit Tests — Risk Narrative Generator (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import RiskNarrativeGenerator


class TestRiskNarrativeGenerator:
    """Mandatory Test Case 3: Risk Narrative generates risk statement with authoritative values."""

    def setup_method(self):
        self.gen = RiskNarrativeGenerator()

    def test_risk_statement_contains_score(self):
        res = self.gen.generate(85.0, "HIGH_RISK", "HIGH", "SUFFICIENT", "NETWORK_THREAT", [], [], [], [])
        assert "85.0" in res.risk_statement

    def test_risk_statement_contains_band(self):
        res = self.gen.generate(85.0, "HIGH_RISK", "HIGH", "SUFFICIENT", "NETWORK_THREAT", [], [], [], [])
        assert "HIGH_RISK" in res.risk_statement

    def test_risk_statement_contains_confidence(self):
        res = self.gen.generate(85.0, "HIGH_RISK", "HIGH", "SUFFICIENT", "NETWORK_THREAT", [], [], [], [])
        assert "HIGH" in res.risk_statement

    def test_primary_risk_explanation(self):
        res = self.gen.generate(85.0, "HIGH_RISK", "HIGH", "SUFFICIENT", "NETWORK_THREAT", [], [], [], [])
        assert "network threat" in res.primary_risk_explanation.lower()

    def test_uncertainty_default(self):
        res = self.gen.generate(5.0, "TRUSTED", "HIGH", "SUFFICIENT", "NETWORK_THREAT", [], [], [], [])
        assert "No significant" in res.uncertainty

    def test_mitigating_factors(self):
        res = self.gen.generate(50.0, "MODERATE_RISK", "MEDIUM", "LIMITED", "DATA_LEAK", [], ["mit1"], [], [])
        assert len(res.mitigating_factors) >= 1
