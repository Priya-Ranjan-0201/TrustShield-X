import pytest
from app.services.security_engineering.security_gap_engine import SecurityGapEngine

def test_threat_driven_improvement():
    engine = SecurityGapEngine()
    g = engine.create_gap(
        title="AP-44 Campaign Drift",
        description="New C2 domain generation algorithm detected in global intelligence",
        source="THREAT_INTELLIGENCE",
    )
    assert g.source == "THREAT_INTELLIGENCE"
