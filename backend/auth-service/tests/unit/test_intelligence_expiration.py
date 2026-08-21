import pytest
from datetime import datetime, timezone, timedelta
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.intelligence_quality_engine import IntelligenceQualityEngine


def test_intelligence_freshness_classification():
    quality_engine = IntelligenceQualityEngine()

    now = datetime.now(timezone.utc)
    fresh_obj = ThreatIntelligenceObjectDTO(
        intelligence_type="IP",
        raw_indicator="192.0.2.1",
        created_at=now.isoformat(),
    )
    score_fresh = quality_engine.evaluate_quality(fresh_obj)
    assert score_fresh.freshness_status == "FRESH"
    assert score_fresh.freshness_score == 1.0

    stale_obj = ThreatIntelligenceObjectDTO(
        intelligence_type="IP",
        raw_indicator="192.0.2.2",
        created_at=(now - timedelta(days=10)).isoformat(),
    )
    score_stale = quality_engine.evaluate_quality(stale_obj)
    assert score_stale.freshness_status == "STALE"
    assert score_stale.freshness_score < 1.0
