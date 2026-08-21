import pytest
from app.services.protected_target_engine import ProtectedTargetEngine, TargetValidationError
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.schemas.autonomous_defense_models import DecisionContextDTO


def test_tenant_boundary_validation_success():
    authorized = ["tenant-a-domain.com", "198.51.100.10"]
    ProtectedTargetEngine.validate_action_target(
        target="tenant-a-domain.com",
        target_type="DOMAIN",
        tenant_id="tenant_a",
        authorized_tenant_targets=authorized,
    )


def test_cross_tenant_target_rejection():
    authorized = ["tenant-a-domain.com"]
    with pytest.raises(TargetValidationError) as exc:
        ProtectedTargetEngine.validate_action_target(
            target="tenant-b-domain.com",
            target_type="DOMAIN",
            tenant_id="tenant_a",
            authorized_tenant_targets=authorized,
        )
    assert "Cross-tenant violation" in str(exc.value)


def test_orchestrator_tenant_plan_isolation():
    orch = AutonomousDefenseOrchestrator()

    ctx = DecisionContextDTO(
        risk_score=85.0,
        severity="HIGH",
        confidence=0.95,
        action_type="BLOCK_DOMAIN",
        target="phish.com",
    )

    plan_a = orch.create_response_plan(
        tenant_id="org_alpha",
        incident_id="inc_001",
        title="Alpha Defense Plan",
        description="Alpha Description",
        threat_contexts=[ctx],
    )

    # Tenant Alpha can access plan
    assert orch.get_plan(plan_a.plan_id, "org_alpha") is not None

    # Tenant Beta CANNOT access or execute Tenant Alpha's plan
    assert orch.get_plan(plan_a.plan_id, "org_beta") is None

    with pytest.raises(KeyError):
        orch.execute_plan(plan_a.plan_id, "org_beta")

    with pytest.raises(KeyError):
        orch.simulate_plan(plan_a.plan_id, "org_beta")
