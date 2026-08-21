import pytest
from app.services.resilience_twin.recovery_simulation_engine import RecoverySimulationEngine


def test_rto_rpo_simulation_metrics():
    engine = RecoverySimulationEngine()
    rec = engine.simulate_recovery(tenant_id="tenant_rto", target_rto=120, target_rpo=30)

    assert rec.target_rto_minutes == 120
    assert rec.target_rpo_minutes == 30
    assert rec.simulated_rpo_minutes <= rec.target_rpo_minutes
