import pytest
from app.services.threat_intelligence_fusion.asset_exposure_correlation_engine import AssetExposureCorrelationEngine

def test_asset_exposure_mapping():
    engine = AssetExposureCorrelationEngine()
    exposed = engine.correlate_asset_exposure(
        indicator_values=["Darkstorm C2 beacon"],
        cve_ids=["CVE-2026-3091"],
        requester_tenant_id="tenant_banking_01"
    )
    assert len(exposed) >= 1
    assert exposed[0]["asset_id"] == "ast_payment_gw_01"
