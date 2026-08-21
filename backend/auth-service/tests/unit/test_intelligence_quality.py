import pytest
from app.services.threat_intelligence.intelligence_quality_engine import IntelligenceQualityEngine


def test_intelligence_quality_scores():
    engine = IntelligenceQualityEngine()
    metrics = engine.compute_quality_metrics()

    assert metrics.completeness_score > 90.0
    assert metrics.freshness_score > 95.0
    assert metrics.provenance_integrity_pct == 100.0
    assert metrics.overall_quality_grade == "GRADE_A"
