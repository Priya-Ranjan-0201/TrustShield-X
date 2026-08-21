import pytest
from app.services.zero_trust_exposure.remediation_validation_engine import RemediationValidationEngine

def test_remediation_independent_verification():
    engine = RemediationValidationEngine()
    
    # Create remediation plan
    plan = engine.create_remediation_plan(
        action_id="ACT-01",
        tenant_id="tenant-alpha",
        exposure_id="EXP-99",
        recommendation_type="PATCH",
        title="Apply OpenSSL Security Patch",
        description="Patch CVE-2024-9999 on APP-PROD",
        composite_risk=9.0
    )
    assert plan["priority"] == "CRITICAL"
    assert plan["validation_status"] == "REMEDIATION_NOT_VERIFIED"
    
    # Unverified attempt
    res1 = engine.verify_remediation("ACT-01", "tenant-alpha", rescan_telemetry=None)
    assert res1["validation_status"] == "REMEDIATION_NOT_VERIFIED"
    
    # Verified with independent scan
    res2 = engine.verify_remediation(
        "ACT-01",
        "tenant-alpha",
        rescan_telemetry={"independent_scan_passed": True, "scanner": "Qualys/Tenable"}
    )
    assert res2["validation_status"] == "CONFIRMED_REMEDIATED"
    assert res2["status"] == "VERIFIED"
