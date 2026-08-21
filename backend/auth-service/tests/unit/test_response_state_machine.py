import pytest
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.schemas.autonomous_defense_models import DecisionContextDTO


def test_deterministic_plan_state_progression():
    orch = AutonomousDefenseOrchestrator()
    ctx = DecisionContextDTO(
        risk_score=85.0,
        severity="HIGH",
        confidence=0.95,
        action_type="BLOCK_DOMAIN",
        target="malicious-tracker.com",
    )

    # 1. State: CREATED
    plan = orch.create_response_plan(
        tenant_id="tenant_1",
        incident_id="inc_sm_01",
        title="State Machine Plan",
        description="Testing state progression",
        threat_contexts=[ctx],
    )
    assert plan.state == "CREATED"
    assert len(plan.actions) == 1
    assert plan.actions[0].state == "CREATED"

    # 2. State: SIMULATED
    sim = orch.simulate_plan(plan.plan_id, "tenant_1")
    assert sim.policy_evaluation_passed is True
    assert plan.state == "SIMULATED"

    # 3. State: AWAITING_APPROVAL
    appr_id = orch.request_action_approval(
        plan_id=plan.plan_id,
        action_id=plan.actions[0].action_id,
        requested_by="analyst_vikram",
        reason="Verified C2 infrastructure",
        tenant_id="tenant_1",
    )
    assert plan.state == "AWAITING_APPROVAL"
    assert plan.actions[0].state == "AWAITING_APPROVAL"

    # 4. State: APPROVED
    orch.approve_action(
        approval_id=appr_id,
        approver_id="lead_neha",
        decision="APPROVED",
        decision_reason="Confirmed high confidence risk",
        tenant_id="tenant_1",
    )
    assert plan.state == "APPROVED"
    assert plan.actions[0].state == "APPROVED"

    # 5. State: EXECUTED
    executed = orch.execute_plan(plan.plan_id, "tenant_1")
    assert plan.state == "EXECUTED"
    assert executed[0].state == "EXECUTED"

    # 6. State: VERIFIED
    verifications = orch.verify_plan(plan.plan_id, "tenant_1")
    assert plan.state == "VERIFIED"
    assert verifications[0].verification_passed is True
    assert plan.actions[0].state == "VERIFIED"
