import pytest
from app.services.resilience_twin.simulation_safety_sandbox import (
    SimulationSafetySandbox,
    SandboxResourceExceededError,
)


def test_simulation_resource_caps():
    sandbox = SimulationSafetySandbox(max_graph_nodes=500)

    with pytest.raises(SandboxResourceExceededError):
        sandbox.validate_simulation_request(node_count=501)

    sandbox.validate_simulation_request(node_count=499)
