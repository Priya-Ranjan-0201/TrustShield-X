import pytest
from app.services.resilience_twin.recovery_simulation_engine import RecoverySimulationEngine


def test_recovery_bottlenecks_detection():
    engine = RecoverySimulationEngine()
    rec = engine.simulate_recovery(tenant_id="tenant_bneck", is_business_mapped=False)

    assert any("BUSINESS_MAPPING_UNKNOWN" in b for b in rec.recovery_bottlenecks)
    assert rec.recovery_path_verified is False
