import pytest
from app.services.global_defense.privacy_sanitization_engine import PrivacySanitizationEngine
from app.services.global_defense.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine

def test_privacy_preserving_end_to_end_evaluation():
    pol_engine = IntelligenceSharingPolicyEngine()
    san_engine = PrivacySanitizationEngine()
    
    pol = pol_engine.evaluate_sharing("default_tenant", "tenant_finance_alpha", "CONFIDENTIAL", "THREAT_DEFENSE")
    assert pol["allowed"] is True
    
    san = san_engine.sanitize_payload({"c2": "evil.org", "internal_host": "192.168.1.100"})
    assert san.sanitized_payload["internal_host"] == "[REDACTED_PRIVATE_IP]"
