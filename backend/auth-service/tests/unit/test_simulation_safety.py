import pytest
from app.services.digital_twin_lab.simulation_isolation_guard import SimulationIsolationGuard

def test_simulation_safety_and_resource_bounds():
    guard = SimulationIsolationGuard()
    res = guard.enforce_isolation("lab_sandbox_cluster")
    assert res["production_mutation_prevented"] is True
    assert res["resource_limits_enforced"]["max_nodes"] == 50
