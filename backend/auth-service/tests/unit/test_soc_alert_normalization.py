"""Unit Tests — SOC Alert Normalization (Phase 4.0 Part 7 — Sections 2-5)."""

import pytest
from app.services.soc.alert_normalization_engine import AlertNormalizationEngine


class TestSOCAlertNormalization:
    def test_normalize_apk_malware_alert(self):
        raw = {
            "id": "raw_apk_01",
            "type": "MALWARE_DETECTION",
            "category": "MALWARE",
            "title": "Trojan.Banker Detected in APK",
            "description": "Suspicious accessibility abuse and overlay injection",
            "severity": "CRITICAL",
            "priority": "HIGH",
            "confidence": "HIGH",
            "entity_ids": ["com.fake.sbi.banking", "hash_dex_1234"],
            "finding_ids": ["fnd_overlay_1"],
        }
        alert = AlertNormalizationEngine.normalize_alert(raw, source_system="INTERNAL_DETECTOR")
        assert alert.source_alert_id == "raw_apk_01"
        assert alert.category == "MALWARE"
        assert alert.severity == "CRITICAL"
        assert alert.priority == "HIGH"
        assert len(alert.entity_ids) == 2

    def test_normalize_voice_clone_alert(self):
        raw = {
            "alert_id": "raw_voice_99",
            "alert_type": "VOICE_CLONE_FRAUD",
            "category": "VOICE",
            "summary": "Neural synthesis voice clone match with 98% similarity",
            "severity": "HIGH",
            "entity_id": "phone_e164_masked",
        }
        alert = AlertNormalizationEngine.normalize_alert(raw, source_system="MODEL_ASSISTED")
        assert alert.category == "VOICE_SCAM"
        assert alert.source_system == "MODEL_ASSISTED"
        assert "phone_e164_masked" in alert.entity_ids

    def test_normalize_phishing_url_alert(self):
        raw = {
            "type": "PHISHING_URL",
            "category": "PHISHING",
            "title": "Credential Harvester URL Match",
            "severity": "HIGH",
            "entity_ids": ["http://phish-secure-login.com"],
        }
        alert = AlertNormalizationEngine.normalize_alert(raw, source_system="THREAT_INTELLIGENCE")
        assert alert.category == "PHISHING"
        assert alert.severity == "HIGH"
