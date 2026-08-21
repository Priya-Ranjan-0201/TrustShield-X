import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_data_redaction_secrets_and_emails():
    engine = CollaborativeDefenseEngine()
    raw = "Incident report by alice@truthshield.internal with api_key='sk_live_999888777'."
    sanitized = engine.redact_pii_and_secrets(raw)

    assert "alice@truthshield.internal" not in sanitized
    assert "[REDACTED_USER_EMAIL]" in sanitized
    assert "sk_live_999888777" not in sanitized
    assert "api_key=[REDACTED_SECRET]" in sanitized
