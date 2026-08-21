import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_action_dry_run_simulation():
    engine = AutonomousDefenseEngine()
    engine.propose_defensive_action("ACT-DRY", "t1", "DEV-01", "QUARANTINE_NON_CRITICAL_ENDPOINT")
    preview = engine.generate_dry_run_preview("ACT-DRY", "t1")
    assert preview["dry_run_passed"] is True
    assert preview["status"] == "PREVIEW"
