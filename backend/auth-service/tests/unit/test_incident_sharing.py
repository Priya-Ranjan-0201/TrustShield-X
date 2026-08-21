import pytest
from app.services.global_defense.privacy_sanitization_engine import PrivacySanitizationEngine

def test_incident_sharing_sanitized_indicators():
    engine = PrivacySanitizationEngine()
    incident_data = {
        "incident_category": "CREDENTIAL_STUFFING",
        "affected_auth_endpoint": "https://auth.internal.corp/token",
        "source_ip": "10.200.1.5",
    }
    res = engine.sanitize_payload(incident_data)
    assert res.sanitized_payload["source_ip"] == "[REDACTED_PRIVATE_IP]"
