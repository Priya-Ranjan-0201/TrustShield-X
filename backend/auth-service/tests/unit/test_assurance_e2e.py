import pytest
from app.services.assurance_fabric.security_assurance_fabric import SecurityAssuranceFabric

def test_phase24_assurance_e2e_lifecycle():
    fabric = SecurityAssuranceFabric()
    # 1. Discover & Inventory Controls
    overview = fabric.get_complete_assurance_overview()
    assert overview["security_controls_count"] >= 3

    # 2. Evaluate Assertions
    assertions = fabric.assertion_engine.list_assertions()
    assert len(assertions) >= 2

    # 3. Test & Validate with SHA-256 Evidence
    val_res = fabric.validation_engine.execute_validation(
        control_id="ctl_tenant_isolation",
        test_name="E2E_TENANT_ISOLATION_TEST",
        expected_result="ACCESS_DENIED",
        actual_result="ACCESS_DENIED",
        has_evidence=True,
    )
    assert val_res.status == "PASS"

    # 4. Dependency Graph & Change-Triggered Regression
    affected = fabric.dependency_graph.get_affected_controls(["app_auth_service"])
    assert "ctl_tenant_isolation" in affected
    reg_run = fabric.regression_engine.run_regression_suite(
        trigger_event="PR_MERGE_AUTH",
        changed_components=["app_auth_service"],
        affected_controls=affected,
        baseline_states={"ctl_tenant_isolation": "PASS", "ctl_four_eyes_response": "PASS"},
        current_test_results={"ctl_tenant_isolation": "PASS", "ctl_four_eyes_response": "PASS"},
    )
    assert reg_run.passed_count == len(affected)

    # 5. Drift Detection & Reconciliation
    drift = fabric.drift_engine.detect_drift("CONFIGURATION", "firewall_port_22", "Open port detected")
    rec = fabric.drift_engine.reconcile_drift(drift.drift_id)
    assert rec.is_reconciled is True

    # 6. AI Assurance & Negative Testing
    ai_res = fabric.ai_assurance_engine.evaluate_ai_safety("Copilot_LLM")
    assert ai_res.status == "PASS"
    neg_res = fabric.negative_testing_engine.test_cross_tenant_isolation("tenant_x", "tenant_y")
    assert neg_res["passed"] is True

    # 7. Remediation & Verification
    rem_plan = fabric.remediation_engine.create_remediation_plan("ctl_1", "Failure", ["Action"])
    approved_rem = fabric.remediation_engine.approve_and_execute(rem_plan.remediation_id, "usr_ciso")
    reval_rem = fabric.remediation_engine.revalidate_remediation(approved_rem.remediation_id, test_passed=True)
    assert reval_rem.execution_status == "REMEDIATED"

    # 8. Scorecard & Maturity
    scorecard = fabric.scorer.evaluate_scorecard()
    assert scorecard.overall_score >= 90.0
    assert scorecard.maturity_level == "LEVEL_5_CONTINUOUSLY_VALIDATED"
