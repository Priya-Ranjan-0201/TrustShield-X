import pytest
from app.services.simulation.environment_execution_guard import EnvironmentExecutionGuard


def test_environment_guard_blocks_real_credentials():
    guard = EnvironmentExecutionGuard()

    # Payload with real live bearer token
    malicious_payload = {"auth_header": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"}

    with pytest.raises(ValueError) as exc_info:
        guard.validate_simulation_action("SIMULATION", "TEST_AUTH", malicious_payload)

    assert "Production secret or private key detected" in str(exc_info.value)
