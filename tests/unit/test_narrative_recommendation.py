"""Unit Tests — Recommendation Explanation Generator (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import RecommendationExplanationGenerator


class TestRecommendationExplanationGenerator:
    """Mandatory Test Case 11: Recommendation Explanation with urgency levels."""

    def setup_method(self):
        self.gen = RecommendationExplanationGenerator()

    def test_critical_risk_recommendation(self):
        stmts = self.gen.generate(["Uninstall the application"], "CRITICAL_RISK")
        assert len(stmts) == 1
        assert "IMMEDIATE" in stmts[0].claim

    def test_high_risk_recommendation(self):
        stmts = self.gen.generate(["Review permissions"], "HIGH_RISK")
        assert "IMMEDIATE" in stmts[0].claim

    def test_moderate_risk_recommendation(self):
        stmts = self.gen.generate(["Monitor behavior"], "MODERATE_RISK")
        assert "HIGH" in stmts[0].claim

    def test_low_risk_recommendation(self):
        stmts = self.gen.generate(["Continue monitoring"], "LOW_RISK")
        assert "MEDIUM" in stmts[0].claim

    def test_empty_input(self):
        stmts = self.gen.generate([], "TRUSTED")
        assert stmts == []
