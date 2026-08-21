import pytest
from app.services.resilience.resilience_gap_engine import ResilienceGapEngine

def test_recovery_recommendations():
    engine = ResilienceGapEngine()
    gaps = engine.detect_gaps(backup_age_hours=30.0, failover_tested=True)
    assert len(gaps) == 1
    assert "automated full snapshot" in gaps[0].recommendation
