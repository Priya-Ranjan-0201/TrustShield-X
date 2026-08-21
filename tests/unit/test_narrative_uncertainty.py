"""Unit Tests — Uncertainty Explanation Generator (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import UncertaintyExplanationGenerator


class TestUncertaintyExplanationGenerator:
    """Mandatory Test Case 12: Uncertainty explanation for low confidence and insufficient evidence."""

    def setup_method(self):
        self.gen = UncertaintyExplanationGenerator()

    def test_low_confidence(self):
        res = self.gen.explain("LOW", "SUFFICIENT", [])
        assert "limited" in res.lower()

    def test_insufficient_evidence(self):
        res = self.gen.explain("HIGH", "INSUFFICIENT", [])
        assert "insufficient" in res.lower()

    def test_unresolved_items(self):
        res = self.gen.explain("HIGH", "SUFFICIENT", ["Item 1"])
        assert "Item 1" in res

    def test_no_uncertainty(self):
        res = self.gen.explain("HIGH", "SUFFICIENT", [])
        assert "No significant" in res
