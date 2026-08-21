import pytest
from app.services.zero_trust_exposure.exposure_management_engine import ExposureManagementEngine

def test_exposure_lifecycle():
    engine = ExposureManagementEngine()
    
    exp = engine.record_exposure(
        exposure_id="EXP-99",
        tenant_id="tenant-alpha",
        asset_id="EXT-1",
        exposure_type="PUBLICLY_REACHABLE",
        severity="HIGH",
        reachability_evidence={"verified_ports": [80, 443]},
        business_impact="HIGH"
    )
    assert exp["status"] == "OPEN"
    assert exp["reachability"] == "REACHABLE"
    
    open_exps = engine.get_open_exposures("tenant-alpha")
    assert len(open_exps) == 1
