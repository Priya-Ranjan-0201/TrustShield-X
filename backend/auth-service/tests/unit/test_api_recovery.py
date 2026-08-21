import pytest
from app.services.resilience.recovery_verification_engine import RecoveryVerificationEngine

def test_api_recovery():
    engine = RecoveryVerificationEngine()
    ver = engine.verify_action("act_api_rec", "ast_api_gateway", expected_state="HTTP_200", actual_state="HTTP_200")
    assert ver.verification_status == "VERIFIED"
    assert ver.divergence_detected is False
