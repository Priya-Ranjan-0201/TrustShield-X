import pytest
from app.services.zero_trust_exposure.zero_trust_security_engine import ZeroTrustSecurityEngine

def test_phase34_full_closed_loop_e2e():
    engine = ZeroTrustSecurityEngine()
    tenant = "tenant-e2e-p34"
    
    # 1. Identity & Device & Session registration
    engine.identity_engine.register_identity("USR-E2E", tenant, "commander", "commander@truthshield.io")
    engine.device_engine.register_device("DEV-E2E", tenant, "USR-E2E", "host-e2e", "macOS", "14.5", edr_active=True, disk_encrypted=True, firewall_active=True)
    engine.session_engine.create_session("SESS-E2E", tenant, "USR-E2E", "DEV-E2E", "10.10.10.10")
    
    # 2. Access Request evaluation
    access = engine.evaluate_unified_access_request(
        tenant_id=tenant,
        subject_id="USR-E2E",
        device_id="DEV-E2E",
        session_id="SESS-E2E",
        resource_id="CROWN-JEWEL-DB",
        resource_sensitivity="RESTRICTED",
        action="ACCESS",
        source_ip="10.10.10.10"
    )
    assert access["decision"] == "ALLOW"
    
    # 3. EASM asset discovery
    asset = engine.easm_engine.discover_asset("EXT-E2E-1", tenant, "api-e2e.truthshield.io", "DOMAIN", open_ports=[443])
    assert asset["asset_id"] == "EXT-E2E-1"
    
    # 4. Exposure & Vulnerability correlation
    exp = engine.exposure_engine.record_exposure("EXP-E2E-1", tenant, "EXT-E2E-1", "PUBLICLY_REACHABLE", severity="HIGH", reachability_evidence={"probe_successful": True})
    assert exp["reachability"] == "REACHABLE"
    
    vuln = engine.vuln_correlation_engine.correlate_vulnerability("VCORR-E2E", tenant, "EXT-E2E-1", "CVE-2024-3094", 10.0, 0.95, "PUBLICLY_REACHABLE", exploit_evidence={"in_the_wild_active_exploitation": True})
    assert vuln["exploitability"] == "VERIFIED"
    
    # 5. Attack Path Analysis
    path = engine.attack_path_engine.analyze_path(
        path_id="PATH-E2E-1",
        tenant_id=tenant,
        entry_point="EXT-E2E-1",
        target_crown_jewel="CROWN-JEWEL-DB",
        evidence=[{"reachability_confirmed": True}]
    )
    assert path["status"] == "VERIFIED"
    
    # 6. Blast Radius calculation
    blast = engine.blast_radius_engine.calculate_blast_radius("EXT-E2E-1", tenant, neighbors=["APP-NODE-1", "APP-NODE-2"], data_stores=["CROWN-JEWEL-DB"])
    assert blast["blast_radius_score"] > 0
    
    # 7. Remediation & Validation
    rem = engine.remediation_engine.create_remediation_plan("REM-E2E-1", tenant, "EXP-E2E-1", "PATCH", "Patch XZ Utils in Gateway", "Update container", composite_risk=9.5)
    assert rem["validation_status"] == "REMEDIATION_NOT_VERIFIED"
    
    # Rescan verification
    rem_verified = engine.remediation_engine.verify_remediation("REM-E2E-1", tenant, {"independent_scan_passed": True, "rescan_timestamp": "2026-08-20T23:55:00Z"})
    assert rem_verified["validation_status"] == "CONFIRMED_REMEDIATED"
    assert rem_verified["status"] == "VERIFIED"
