import pytest
from app.services.threat_intelligence_fusion.asset_exposure_correlation_engine import AssetExposureCorrelationEngine

def test_cross_tenant_intelligence_isolation():
    engine = AssetExposureCorrelationEngine()
    res_deny = engine.verify_tenant_isolation(
        requester_tenant_id="tenant_alpha",
        target_intelligence_tenant="tenant_beta",
        classification="CONFIDENTIAL"
    )
    assert res_deny["allowed"] is False
    assert "TENANT_ISOLATION_VIOLATION" in res_deny["reason"]
    
    res_allow = engine.verify_tenant_isolation(
        requester_tenant_id="tenant_alpha",
        target_intelligence_tenant="tenant_alpha"
    )
    assert res_allow["allowed"] is True
