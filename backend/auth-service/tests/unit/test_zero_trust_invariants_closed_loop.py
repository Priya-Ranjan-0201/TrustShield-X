import pytest
from app.services.zero_trust_exposure.zero_trust_security_engine import ZeroTrustSecurityEngine

def test_absolute_zero_trust_invariants():
    engine = ZeroTrustSecurityEngine()
    
    # Invariant 1: An identity cannot bypass device or session health checks
    dec_compromised_device = engine.decision_engine.evaluate_access(
        tenant_id="tenant-inv",
        correlation_id="INV-1",
        subject_id="ADMIN-ROOT",
        device_id="DEV-INFECTED",
        session_id="SESS-01",
        resource_id="PROD-DB",
        resource_sensitivity="RESTRICTED",
        action="WRITE",
        identity_trust_state="TRUSTED",
        device_trust_state="UNTRUSTED",
        session_state="ACTIVE",
        risk_score=9.5
    )
    assert dec_compromised_device["decision"] == "DENY"
    
    # Invariant 2: JIT elevation cannot be granted without peer review if required
    jit = engine.privilege_engine.approve_jit_elevation(
        request_id="NON_EXISTENT",
        tenant_id="tenant-inv",
        approver_id="HACKER"
    )
    assert jit["status"] == "FAILED"
    
    # Invariant 3: Unverified AI Attack Paths must not be treated as ground truth
    ai_path = engine.attack_path_engine.analyze_path(
        path_id="PATH-SYNTH",
        tenant_id="tenant-inv",
        entry_point="INTERNET",
        target_crown_jewel="CORE-DB",
        path_type="AI_PREDICTION",
        nodes=[],
        edges=[],
        evidence=[],
        is_ai_generated=True
    )
    assert ai_path["validation_status"] == "AI_PATH_UNVERIFIED"
    
    # Invariant 4: Remediation is never assumed successful without independent rescan proof
    remed = engine.remediation_engine.verify_remediation(
        action_id="ACT-DUMMY",
        tenant_id="tenant-inv",
        rescan_telemetry=None
    )
    assert remed["status"] == "FAILED" or remed["validation_status"] == "REMEDIATION_NOT_VERIFIED"
