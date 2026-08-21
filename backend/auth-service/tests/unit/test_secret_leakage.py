import pytest
from app.services.global_defense.privacy_sanitization_engine import PrivacySanitizationEngine

def test_secret_leakage_detection_and_redaction():
    engine = PrivacySanitizationEngine()
    dirty_payload = {"api_key": "sk_test_secret_12345", "auth_token": "bearer_jwt_secret_token"}
    san = engine.sanitize_payload(dirty_payload)
    assert san.sanitized_payload["api_key"] == "[REDACTED_SECRET]"
    assert san.sanitized_payload["auth_token"] == "[REDACTED_SECRET]"
