import pytest
from app.services.global_defense.privacy_sanitization_engine import PrivacySanitizationEngine

def test_sanitization_validation_verified_clean():
    engine = PrivacySanitizationEngine()
    clean_payload = {"indicator": "198.51.100.22", "asn": "AS-64496"}
    res = engine.sanitize_payload(clean_payload)
    assert res.verified_clean is True
    assert res.redacted_fields_count == 0
