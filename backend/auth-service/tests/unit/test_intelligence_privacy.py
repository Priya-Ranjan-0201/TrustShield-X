import pytest
from app.services.federation.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine


def test_pii_field_redaction():
    engine = IntelligenceSharingPolicyEngine()

    payload = {
        "threat_indicator": "phish-drop.com",
        "victim_email": "target_user@bank.com",
        "victim_phone": "555-123-4567",
    }

    redacted = engine.redact_pii_fields(payload)
    assert redacted["threat_indicator"] == "phish-drop.com"
    assert "[REDACTED_EMAIL]" in redacted["victim_email"]
    assert "[REDACTED_PHONE]" in redacted["victim_phone"]
