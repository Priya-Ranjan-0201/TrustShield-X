import pytest
from app.services.resilience.cyber_resilience_engine import CyberResilienceEngine

def test_resilience_e2e_lifecycle():
    engine = CyberResilienceEngine()
    # 1. Assess & Model
    overview = engine.get_complete_resilience_overview()
    assert overview["critical_services_count"] >= 1

    # 2. Simulate Attack
    sim = engine.twin_engine.simulate_attack_and_disruption("ast_pg_primary")
    assert sim["mode"] == "SIMULATED"

    # 3. Detect Gaps
    gaps = engine.gap_engine.detect_gaps(backup_age_hours=2.0, failover_tested=True)
    assert isinstance(gaps, list)

    # 4. Plan & Authorize Recovery
    plan = engine.plan_engine.generate_plan("svc_checkout_api", ["ast_pg_primary", "ast_api_gateway"])
    approved_plan = engine.plan_engine.approve_plan(plan.plan_id, "usr_ciso")
    assert approved_plan.is_approved is True

    # 5. Execute Recovery Step
    exec_res = engine.execution_engine.execute_step(
        plan=approved_plan,
        step_id=approved_plan.steps[0].step_id,
        target="ast_pg_primary",
        action="RESTORE_STANDBY",
        requester_id="usr_sre",
        approver_id="usr_ciso",
        target_environment="ISOLATED_SANDBOX",
    )
    assert exec_res.execution_state == "EXECUTED"

    # 6. Verify & Validate Business Workflow
    ver_res = engine.verification_engine.verify_action(exec_res.recovery_action_id, "ast_pg_primary")
    assert ver_res.verification_status == "VERIFIED"
    bval = engine.business_validation_engine.execute_synthetic_workflow("svc_checkout_api")
    assert bval.workflow_status == "VALIDATED"

    # 7. DR Drill & RPO/RTO
    drill = engine.drill_engine.schedule_drill("DATABASE_RESTORE", environment="ISOLATED_SANDBOX")
    completed_drill = engine.drill_engine.complete_drill(drill.drill_id, measured_rto=14.5, measured_rpo=4.2)
    assert completed_drill.status == "COMPLETED"

    rto_res = engine.rpo_rto_engine.evaluate_rto("svc_checkout_api", 30, completed_drill.measured_rto_minutes, is_empirically_tested=True)
    rpo_res = engine.rpo_rto_engine.evaluate_rpo("svc_checkout_api", 15, completed_drill.measured_rpo_minutes, is_empirically_tested=True)
    assert rto_res.validation_status == "VERIFIED"
    assert rpo_res.validation_status == "VERIFIED"

    # 8. Scorecard
    scorecard = engine.score_engine.evaluate_scorecard()
    assert scorecard.overall_score >= 90.0
    assert scorecard.maturity_level == "LEVEL_5_CONTINUOUSLY_VALIDATED"
