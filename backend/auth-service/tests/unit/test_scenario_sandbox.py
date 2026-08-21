import pytest
from app.services.resilience_twin.simulation_safety_sandbox import (
    SimulationSafetySandbox,
    SandboxSecurityViolationError,
)


def test_scenario_sandbox_secret_isolation():
    sandbox = SimulationSafetySandbox()

    # Reject simulation containing production secrets
    with pytest.raises(SandboxSecurityViolationError):
        sandbox.validate_simulation_request(node_count=10, contains_prod_secrets=True)

    # Valid simulation passes
    sandbox.validate_simulation_request(node_count=10, contains_prod_secrets=False)
