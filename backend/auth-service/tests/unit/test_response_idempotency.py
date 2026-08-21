import pytest
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.schemas.autonomous_defense_models import DecisionContextDTO


def test_idempotent_action_execution():
    orch = AutonomousDefenseOrchestrator()
    ctx = DecisionContextDTO(
        risk_score=50.0,
        confidence=0.85,
        action_type="MARK_INDICATOR",
        target="suspicious-c2.net",
    )

    plan = orch.create_response_plan(
        tenant_id="tenant_idem",
        incident_id="inc_idem",
        title="Idempotency Plan",
        description="Testing idempotency deduplication",
        threat_contexts=[ctx],
    )

    # First execution
    exec1 = orch.execute_plan(plan.plan_id, "tenant_idem")
    assert len(exec1) == 1
    assert exec1[0].state == "EXECUTED"

    # Second duplicate execution with same idempotency key returns existing record without re-executing
    exec2 = orch.execute_plan(plan.plan_id, "tenant_idem")
    assert len(exec2) == 1
    assert exec2[0].action_id == exec1[0].action_id
    assert exec2[0].idempotency_key == exec1[0].idempotency_key
