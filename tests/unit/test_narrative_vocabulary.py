"""Unit Tests — Controlled Vocabulary Enforcement (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import CONTROLLED_VOCABULARY, CERTAINTY_STATES, CLAIM_STRENGTH_ORDER, RISK_BAND_LANGUAGE


class TestControlledVocabulary:
    """Test controlled vocabulary and certainty states are properly defined."""

    def test_controlled_vocabulary_keys(self):
        assert "malicious" in CONTROLLED_VOCABULARY
        assert "steals_data" in CONTROLLED_VOCABULARY
        assert "safe" in CONTROLLED_VOCABULARY

    def test_certainty_states(self):
        assert "DETECTED" in CERTAINTY_STATES
        assert "NOT_DETECTED" in CERTAINTY_STATES
        assert "UNKNOWN" in CERTAINTY_STATES
        assert "CONFLICTED" in CERTAINTY_STATES

    def test_claim_strength_order(self):
        assert CLAIM_STRENGTH_ORDER[0] == "DIRECTLY_OBSERVED"
        assert "UNKNOWN" in CLAIM_STRENGTH_ORDER

    def test_risk_band_language(self):
        assert "TRUSTED" in RISK_BAND_LANGUAGE
        assert "CRITICAL_RISK" in RISK_BAND_LANGUAGE
        assert "no significant" in RISK_BAND_LANGUAGE["TRUSTED"].lower()
