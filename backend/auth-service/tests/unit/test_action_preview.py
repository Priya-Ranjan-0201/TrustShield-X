import pytest
from app.services.cyber_digital_twin.autonomous_defense_engine import AutonomousDefenseEngine

def test_action_preview_details():
    engine = AutonomousDefenseEngine()
    engine.propose_defensive_action("ACT-PREV", "t1", "WAF-01", "BLOCK_SUSPICIOUS_IP_ON_WAF")
    preview = engine.generate_dry_run_preview("ACT-PREV", "t1")
    assert "simulated_effect" in preview
    assert "rollback_method" in preview
