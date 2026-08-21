import pytest
from app.services.enterprise_governance.enterprise_governance_engine import EnterpriseGovernanceEngine

def test_enterprise_governance_e2e_lifecycle():
    engine = EnterpriseGovernanceEngine()
    
    # 1. Control Catalog & Testing
    ctrl = engine.control_catalog.get_control("ctrl_iam_mfa_enforcement")
    assert ctrl is not None
    test_res = engine.control_testing.test_control_effectiveness(ctrl.control_id)
    assert test_res["test_result"] == "PASSED"
    
    # 2. Evidence Integrity Check
    ev_res = engine.evidence_engine.verify_evidence_integrity("evd_iam_mfa_config_dump", "c782b6b0c2e718b5b5c92ef9481283d5a498b375b485d99bfa210940562e84c9")
    assert ev_res["is_valid"] is True
    
    # 3. Policy Evaluation (Explicit Deny Wins)
    pol_res = engine.policy_engine.evaluate_policy_decision("ANALYST", "keys:export", ["ALLOW", "DENY"])
    assert pol_res["decision"] == "DENIED"
    
    # 4. Requirement Mapping
    req = engine.requirement_registry.get_requirement("req_iso27001_a9_4_2")
    assert req is not None
    assert "ctrl_iam_mfa_enforcement" in req.mapped_controls
    
    # 5. Risk Acceptance Enforcement
    rsk_res = engine.risk_engine.evaluate_risk_acceptance("rsk_unauthorized_admin_access", "CISO", "Valid rationale", "2026-09-01T00:00:00Z")
    assert rsk_res["allowed"] is True
    
    # 6. Remediation Validation Gate
    rem_res = engine.remediation_engine.attempt_close_remediation("rem_svc_account_oauth2", is_empirically_validated=True)
    assert rem_res["allowed"] is True
    
    # 7. Third-Party Vendor Data Access
    vnd_res = engine.third_party_engine.evaluate_vendor_data_access("vnd_cloud_storage_aws", "CONFIDENTIAL_ENCRYPTED")
    assert vnd_res["allowed"] is True
    
    # 8. Continuous Assurance Drift Event
    drift_res = engine.assurance_engine.trigger_change_based_reassessment("ctrl_iam_mfa_enforcement", "LIVE_TELEMETRY", True)
    assert drift_res["status"] == "ASSURANCE_MAINTAINED"
    
    # 9. Executive Governance Summary
    summary = engine.get_executive_governance_summary("default_tenant")
    assert summary["compliance_posture"] == "CONTINUOUSLY_ASSURED"
    assert summary["total_controls"] >= 2
