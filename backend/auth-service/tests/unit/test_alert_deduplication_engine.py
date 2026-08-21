import pytest
from app.services.autonomous_defense.alert_optimization_engine import AlertOptimizationEngine

def test_alert_deduplication_same_entity_time():
    engine = AlertOptimizationEngine()
    raw = [
        {"event_type": "DNS_SPIKE", "entity_id": "ast_api_gw", "time_bucket": "t1"},
        {"event_type": "DNS_SPIKE", "entity_id": "ast_api_gw", "time_bucket": "t1"},
        {"event_type": "DNS_SPIKE", "entity_id": "ast_db_cluster", "time_bucket": "t1"},
    ]
    res = engine.deduplicate_alerts(raw)
    assert res["total_raw"] == 3
    assert res["deduplicated_count"] == 2
    assert res["suppressed_count"] == 1
