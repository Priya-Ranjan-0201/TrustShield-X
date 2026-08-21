import pytest
from app.services.global_defense.privacy_sanitization_engine import PrivacySanitizationEngine

def test_automatic_secret_and_ip_sanitization():
    engine = PrivacySanitizationEngine()
    payload = {
        "c2_url": "https://darkstorm.c2/gate",
        "internal_ip": "10.0.12.45",
        "analyst_email": "analyst@bank.com",
        "api_token": "sk_live_99281726481",
    }
    res = engine.sanitize_payload(payload)
    assert res.sanitization_status == "SANITIZED"
    assert res.sanitized_payload["internal_ip"] == "[REDACTED_PRIVATE_IP]"
    assert res.sanitized_payload["analyst_email"] == "[REDACTED_PII]"
    assert res.sanitized_payload["api_token"] == "[REDACTED_SECRET]"
    assert res.redacted_fields_count >= 3
