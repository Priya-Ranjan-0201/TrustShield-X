import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_dr_engine():
    engine = DisasterRecoveryDrillEngine()
    drills = engine.list_drills()
    assert len(drills) >= 1
