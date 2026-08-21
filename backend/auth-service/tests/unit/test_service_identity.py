import pytest
from app.services.zero_trust_exposure.service_identity_engine import ServiceIdentityEngine

def test_spiffe_mtls_validation():
    engine = ServiceIdentityEngine()
    
    # Register SPIFFE service
    svc = engine.register_service(
        service_id="SVC-AI-AGENT",
        tenant_id="tenant-alpha",
        spiffe_id="spiffe://tenant-alpha.prod/ns/security/sa/ai-agent",
        service_name="AI Agent Dispatcher",
        allowed_callers=["spiffe://tenant-alpha.prod/ns/security/sa/gateway"]
    )
    assert svc["mtls_enforced"] is True
    
    # Verify allowed caller
    res1 = engine.verify_service_caller(
        service_id="SVC-AI-AGENT",
        tenant_id="tenant-alpha",
        caller_spiffe_id="spiffe://tenant-alpha.prod/ns/security/sa/gateway",
        mtls_verified=True
    )
    assert res1["authorized"] is True
    
    # Verify unauthorized caller
    res2 = engine.verify_service_caller(
        service_id="SVC-AI-AGENT",
        tenant_id="tenant-alpha",
        caller_spiffe_id="spiffe://tenant-alpha.prod/ns/untrusted/sa/anon",
        mtls_verified=True
    )
    assert res2["authorized"] is False
    assert res2["reason"] == "UNAUTHORIZED_SERVICE_CALLER"
