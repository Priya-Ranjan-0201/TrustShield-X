import pytest
from app.services.autonomous_defense.action_verification_engine import ActionVerificationEngine

def test_action_verification_matching_telemetry():
    engine = ActionVerificationEngine()
    res = engine.verify_action("act_01", "ast_api_gw", "WAF rate limit", "WAF rate limit active", telemetry_matches=True)
    assert res.is_verified is True
    assert res.verification_status == "VERIFIED"
