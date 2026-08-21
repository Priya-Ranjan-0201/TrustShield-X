import pytest
from app.services.mission_control_os.state_conflict_resolution_engine import StateConflictResolutionEngine

def test_state_conflict_preservation():
    engine = StateConflictResolutionEngine()
    cnf = engine.register_state_conflict(
        entity_type="ASSET",
        entity_id="ast_api_gw",
        subsystem_a="SOAR",
        state_a="ISOLATED",
        subsystem_b="ASSET_INVENTORY",
        state_b="ACTIVE_ONLINE",
    )
    assert cnf.status == "STATE_CONFLICT"
    assert len(engine.list_conflicts()) >= 1
