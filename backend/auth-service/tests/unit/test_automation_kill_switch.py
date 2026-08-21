import pytest
from app.services.adaptive_defense.defense_circuit_breaker import DefenseCircuitBreaker


def test_emergency_automation_kill_switch():
    breaker = DefenseCircuitBreaker()
    tenant = "tenant_kill_test"

    assert breaker.can_execute_automated_action(tenant, "action_1") is True

    # Activate emergency kill switch
    breaker.activate_kill_switch(tenant, "SOC_LEAD_ALICE")
    ctrl = breaker.get_or_create_control_state(tenant)
    assert ctrl.kill_switch_active is True
    assert ctrl.automation_enabled is False
    assert breaker.can_execute_automated_action(tenant, "action_2") is False

    # Deactivate
    breaker.deactivate_kill_switch(tenant, "SOC_LEAD_ALICE")
    assert breaker.can_execute_automated_action(tenant, "action_2") is True
