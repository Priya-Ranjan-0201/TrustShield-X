import pytest
from app.services.resilience.recovery_verification_engine import RecoveryVerificationEngine

def test_resilience_audit():
    engine = RecoveryVerificationEngine()
    ver = engine.verify_action("act_audit", "ast_pg_primary")
    assert ver.evidence_reference.startswith("ev_dr_ver_")
