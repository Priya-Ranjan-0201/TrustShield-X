import pytest
from app.services.federation.intelligence_sharing_policy_engine import IntelligenceSharingPolicyEngine


def test_secret_detection_and_blocking():
    engine = IntelligenceSharingPolicyEngine()

    sample_with_bearer = "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.abcdef"
    secrets = engine.detect_secrets(sample_with_bearer)
    assert len(secrets) > 0
    assert "BEARER_TOKEN" in secrets

    decision = engine.evaluate_sharing({"auth_header": sample_with_bearer})
    assert decision.decision == "REJECT"
