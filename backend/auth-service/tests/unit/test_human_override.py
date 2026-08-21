import pytest
from app.services.adaptive_defense.defense_circuit_breaker import DefenseCircuitBreaker


def test_human_operator_override_pausing():
    breaker = DefenseCircuitBreaker()
    tenant = "tenant_pause_test"

    ctrl = breaker.get_or_create_control_state(tenant)
    ctrl.automation_enabled = False
    ctrl.last_modified_by = "ANALYST_BOB"

    assert breaker.can_execute_automated_action(tenant, "action_x") is False
