import pytest
from app.services.resilience.dr_drill_engine import DisasterRecoveryDrillEngine

def test_drill_safety():
    engine = DisasterRecoveryDrillEngine()
    with pytest.raises(ValueError, match="Drill Safety Violation"):
        engine.schedule_drill("DATABASE_RESTORE", environment="PRODUCTION")
