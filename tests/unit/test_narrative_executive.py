"""Unit Tests — Executive Summary Generator (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import ExecutiveSummaryGenerator


class TestExecutiveSummaryGenerator:
    """Mandatory Test Case 2: Executive Summary generates headline, assessment, action."""

    def setup_method(self):
        self.gen = ExecutiveSummaryGenerator()

    def test_trusted_band(self):
        res = self.gen.generate(5.0, "TRUSTED", "HIGH", "SUFFICIENT", [], [])
        assert "Trusted" in res.headline
        assert "no significant" in res.overall_assessment.lower()
        assert "no immediate action" in res.recommended_action.lower()

    def test_high_risk_band(self):
        res = self.gen.generate(85.0, "HIGH_RISK", "HIGH", "SUFFICIENT", [], [])
        assert "High Risk" in res.headline
        assert "immediate review" in res.recommended_action.lower()

    def test_critical_risk_band(self):
        res = self.gen.generate(95.0, "CRITICAL_RISK", "HIGH", "SUFFICIENT", [], [])
        assert "Critical Risk" in res.headline
        assert "immediate" in res.recommended_action.lower()

    def test_moderate_risk_band(self):
        res = self.gen.generate(50.0, "MODERATE_RISK", "MEDIUM", "LIMITED", [], [])
        assert "Moderate Risk" in res.headline
        assert "further review" in res.recommended_action.lower()

    def test_low_risk_band(self):
        res = self.gen.generate(20.0, "LOW_RISK", "HIGH", "SUFFICIENT", [], [])
        assert "Low Risk" in res.headline

    def test_confidence_statement(self):
        res = self.gen.generate(50.0, "MODERATE_RISK", "MEDIUM", "LIMITED", [], [])
        assert "MEDIUM" in res.confidence_statement
        assert "limited" in res.confidence_statement.lower()

    def test_limitations_present(self):
        res = self.gen.generate(5.0, "TRUSTED", "HIGH", "SUFFICIENT", [], ["Limitation A"])
        assert "Limitation A" in res.limitations
