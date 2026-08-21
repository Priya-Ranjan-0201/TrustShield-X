import pytest
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.schemas.autonomous_defense_models import DecisionContextDTO
from app.services.soc.response_adapters import DNSResponseAdapter


def test_successful_action_rollback():
    dns_adapter = DNSResponseAdapter()
    orch = AutonomousDefenseOrchestrator(adapters={"BLOCK_DOMAIN": dns_adapter})

    ctx = DecisionContextDTO(
        risk_score=85.0,
        severity="HIGH",
        confidence=0.95,
        action_type="BLOCK_DOMAIN",
        target="rollback-domain.com",
    )

    plan = orch.create_response_plan(
        tenant_id="tenant_rol",
        incident_id="inc_rol_01",
        title="Rollback Test Plan",
        description="Verify successful action rollback",
        threat_contexts=[ctx],
    )

    # Approve and execute
    plan.actions[0].approval_status = "APPROVED"
    plan.actions[0].state = "APPROVED"
    orch.execute_plan(plan.plan_id, "tenant_rol")
    assert "rollback-domain.com" in dns_adapter.blocked_domains

    # Execute rollback
    action_id = plan.actions[0].action_id
    rol_res = orch.rollback_action(plan.plan_id, action_id, "tenant_rol", executed_by="soc_lead_arjun")
    assert rol_res.rollback_status == "ROLLED_BACK"
    assert "rollback-domain.com" not in dns_adapter.blocked_domains


def test_rollback_unavailable_reported_explicitly():
    unsupported_adapter = DNSResponseAdapter(simulate_unsupported_rollback=True)
    orch = AutonomousDefenseOrchestrator(adapters={"BLOCK_DOMAIN": unsupported_adapter})

    ctx = DecisionContextDTO(
        risk_score=85.0,
        severity="HIGH",
        confidence=0.95,
        action_type="BLOCK_DOMAIN",
        target="no-rollback.com",
    )

    plan = orch.create_response_plan(
        tenant_id="tenant_no_rol",
        incident_id="inc_no_rol_01",
        title="No Rollback Plan",
        description="Verify explicit ROLLBACK_UNAVAILABLE status",
        threat_contexts=[ctx],
    )

    plan.actions[0].approval_status = "APPROVED"
    plan.actions[0].state = "APPROVED"
    orch.execute_plan(plan.plan_id, "tenant_no_rol")

    action_id = plan.actions[0].action_id
    rol_res = orch.rollback_action(plan.plan_id, action_id, "tenant_no_rol")
    assert rol_res.rollback_status == "ROLLBACK_UNAVAILABLE"
    assert "ROLLBACK_UNAVAILABLE" in rol_res.reason
