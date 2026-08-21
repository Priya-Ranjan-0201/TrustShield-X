"""Unit Tests — Technical, User-Friendly, Analyst Summary Generators (Phase 4.0 Part 2)."""

import pytest
from types import SimpleNamespace
from app.services.trust_narrative_engine import TechnicalSummaryGenerator, UserFriendlySummaryGenerator, AnalystSummaryGenerator


class TestTechnicalSummaryGenerator:
    """Mandatory Test Case 20a: Technical Summary generates engine version and risk info."""

    def setup_method(self):
        self.gen = TechnicalSummaryGenerator()

    def test_technical_summary(self):
        doc = SimpleNamespace(trust_overview=SimpleNamespace(risk_score=50.0, risk_band="MODERATE_RISK"))
        res = self.gen.generate(doc)
        assert "50.0" in res
        assert "MODERATE_RISK" in res
        assert "Engine v1.0.0" in res


class TestUserFriendlySummaryGenerator:
    """Mandatory Test Case 20b: User-Friendly Summary avoids jargon."""

    def setup_method(self):
        self.gen = UserFriendlySummaryGenerator()

    def test_safe_summary(self):
        doc = SimpleNamespace(trust_overview=SimpleNamespace(risk_score=10.0, risk_band="TRUSTED"))
        res = self.gen.generate(doc)
        assert "no immediate action" in res.lower() or "not find significant" in res.lower()

    def test_high_risk_summary(self):
        doc = SimpleNamespace(trust_overview=SimpleNamespace(risk_score=85.0, risk_band="HIGH_RISK"))
        res = self.gen.generate(doc)
        assert "immediate review" in res.lower()

    def test_moderate_summary(self):
        doc = SimpleNamespace(trust_overview=SimpleNamespace(risk_score=50.0, risk_band="MODERATE_RISK"))
        res = self.gen.generate(doc)
        assert "further assessment" in res.lower()


class TestAnalystSummaryGenerator:
    """Mandatory Test Case 20c: Analyst Summary includes finding IDs and provenance."""

    def setup_method(self):
        self.gen = AnalystSummaryGenerator()

    def test_analyst_summary(self):
        doc = SimpleNamespace(trust_overview=SimpleNamespace(risk_score=75.0, risk_band="HIGH_RISK"))
        findings = [SimpleNamespace(finding_id="f1"), SimpleNamespace(finding_id="f2")]
        res = self.gen.generate(doc, findings)
        assert "f1" in res
        assert "f2" in res
        assert "Provenance" in res or "provenance" in res.lower()
