import pytest
from app.services.ai_governance.ai_tenant_privacy_engine import AITenantPrivacyEngine

def test_data_leakage_sanitization():
    engine = AITenantPrivacyEngine()
    sanitized = engine.sanitize_prompt_secrets("Here is the key: sk-live-123456789")
    assert "[REDACTED_SECRET]" in sanitized
