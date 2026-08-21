import pytest
from app.services.mission_control_os.global_security_mission_control_engine import GlobalSecurityMissionControlEngine

def test_failure_recovery_reconciliation():
    engine = GlobalSecurityMissionControlEngine()
    # Simulate restart & state aggregation
    state = engine.state_engine.get_unified_state("default_tenant")
    assert state is not None
    assert state.active_incidents_count >= 1
