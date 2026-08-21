import pytest
from app.services.zero_trust_exposure.service_identity_engine import ServiceIdentityEngine

def test_m2m_authorization_success():
    engine = ServiceIdentityEngine()
    engine.register_service("SRV-A", "t1", "auth-service", "spiffe://prod/auth", allowed_callers=["api-gateway"])
    engine.register_service("SRV-B", "t1", "api-gateway", "spiffe://prod/gw")
    
    res = engine.authorize_m2m_request("SRV-B", "SRV-A", "t1", "CALL_API", mtls_verified=True)
    assert res["decision"] == "ALLOW"

def test_m2m_authorization_unauthorized_caller():
    engine = ServiceIdentityEngine()
    engine.register_service("SRV-A", "t1", "auth-service", "spiffe://prod/auth", allowed_callers=["api-gateway"])
    engine.register_service("SRV-C", "t1", "untrusted-worker", "spiffe://prod/worker")
    
    res = engine.authorize_m2m_request("SRV-C", "SRV-A", "t1", "CALL_API", mtls_verified=True)
    assert res["decision"] == "DENY"
    assert res["reason"] == "CALLER_NOT_IN_TARGET_ALLOWLIST"
