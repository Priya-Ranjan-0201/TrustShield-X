import pytest
from app.services.security_engineering.security_gap_engine import SecurityGapEngine

def test_resilience_improvement():
    engine = SecurityGapEngine()
    g = engine.create_gap(
        title="Slow Replica Sync in Secondary DC",
        description="RTO exceeded target by 15 seconds during resilience drill",
        source="RESILIENCE_TEST",
    )
    assert g.source == "RESILIENCE_TEST"
