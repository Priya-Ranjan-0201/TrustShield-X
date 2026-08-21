import pytest
from app.services.resilience_twin.recovery_simulation_engine import RecoverySimulationEngine


def test_disaster_recovery_simulation():
    engine = RecoverySimulationEngine()
    rec = engine.simulate_recovery(
        tenant_id="tenant_dr",
        target_rto=60,
        target_rpo=15,
        has_empirical_data=True,
    )

    assert rec.target_rto_minutes == 60
    assert rec.empirical_rto_minutes == 75
    assert rec.simulated_rto_minutes == 68
    assert rec.label == "SIMULATED"
    assert len(rec.recovery_bottlenecks) >= 1
