import pytest
from app.services.simulation.disaster_recovery_simulation_engine import DisasterRecoverySimulationEngine


def test_dr_twin_redis_worker_failover():
    engine = DisasterRecoverySimulationEngine()

    dr_redis = engine.simulate_component_failover("REDIS", "CACHE_OUTAGE")
    assert dr_redis.component_tested == "REDIS"
    assert dr_redis.status == "RECOVERED_SIMULATION"

    dr_worker = engine.simulate_component_failover("WORKER", "TASK_DEADLOCK")
    assert dr_worker.component_tested == "WORKER"
    assert dr_worker.status == "RECOVERED_SIMULATION"
