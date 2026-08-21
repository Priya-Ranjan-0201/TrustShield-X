import pytest
from app.services.digital_twin_lab.simulation_isolation_guard import SimulationIsolationGuard

def test_simulation_isolation_zero_production_mutation():
    guard = SimulationIsolationGuard()
    with pytest.raises(PermissionError, match="Simulation Mutation Blocked"):
        guard.enforce_isolation("prod_postgresql_cluster", write_attempt=True)
