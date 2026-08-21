"""Unit Tests — Multilingual Support (Phase 4.0 Part 2)."""

import pytest
from app.services.trust_narrative_engine import RISK_BAND_TRANSLATIONS


class TestMultilingualSupport:
    """Test English, Hindi, and Punjabi translations."""

    def test_english_translations(self):
        assert RISK_BAND_TRANSLATIONS["en"]["TRUSTED"] == "Trusted"
        assert RISK_BAND_TRANSLATIONS["en"]["CRITICAL_RISK"] == "Critical Risk"

    def test_hindi_translations(self):
        assert "विश्वसनीय" in RISK_BAND_TRANSLATIONS["hi"]["TRUSTED"]
        assert "गंभीर" in RISK_BAND_TRANSLATIONS["hi"]["CRITICAL_RISK"]

    def test_punjabi_translations(self):
        assert "ਭਰੋਸੇਮੰਦ" in RISK_BAND_TRANSLATIONS["pa"]["TRUSTED"]
        assert "ਗੰਭੀਰ" in RISK_BAND_TRANSLATIONS["pa"]["CRITICAL_RISK"]

    def test_all_bands_translated(self):
        for lang in ["en", "hi", "pa"]:
            for band in ["TRUSTED", "LOW_RISK", "MODERATE_RISK", "HIGH_RISK", "CRITICAL_RISK"]:
                assert band in RISK_BAND_TRANSLATIONS[lang]
