import pytest
from app.services.security_engineering.security_gap_engine import SecurityGapEngine

def test_security_gap_discovery_and_scoring():
    engine = SecurityGapEngine()
    gaps = engine.list_gaps()
    assert len(gaps) >= 1
    g = engine.create_gap(
        title="Unmonitored LSASS Injection",
        description="Missing endpoint telemetry rule for LSASS read access",
        source="THREAT_INTELLIGENCE",
        severity="HIGH",
        exploitability=0.9,
        exposure=0.8,
        business_impact=0.9,
        likelihood=0.8,
    )
    assert g.total_gap_score >= 8.0
