import pytest
from app.services.resilience_twin.simulation_safety_sandbox import (
    SimulationSafetySandbox,
    SandboxSecurityViolationError,
)


def test_twin_security_production_credential_guard():
    sandbox = SimulationSafetySandbox()

    with pytest.raises(SandboxSecurityViolationError):
        sandbox.validate_simulation_request(node_count=20, contains_prod_secrets=True)
