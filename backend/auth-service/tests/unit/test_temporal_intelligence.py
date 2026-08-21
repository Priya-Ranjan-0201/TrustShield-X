import pytest
from app.services.threat_intelligence.intelligence_quality_engine import IntelligenceQualityEngine


def test_temporal_intelligence_decay():
    engine = IntelligenceQualityEngine()

    # Fast decay for IPs (half-life 7 days)
    decay_ip_7d = engine.calculate_decay("IP", age_days=7)
    assert decay_ip_7d == 0.5

    # Slow decay for CVEs (half-life 365 days)
    decay_cve_7d = engine.calculate_decay("VULNERABILITY", age_days=7)
    assert decay_cve_7d > 0.95
