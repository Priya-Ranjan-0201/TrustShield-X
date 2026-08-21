import pytest
from app.services.hunting.threat_hunt_query_engine import ThreatHuntQueryEngine


def test_hunt_dsl_query_execution():
    engine = ThreatHuntQueryEngine()

    telemetry = [
        {"asset": "api.prod.corp", "exposure_score": 75.0, "new_infrastructure": True},
        {"asset": "db.internal", "exposure_score": 20.0, "new_infrastructure": False},
        {"asset": "staging.corp", "exposure_score": 55.0, "new_infrastructure": True},
    ]
    engine.populate_test_telemetry("tenant_dsl_test", telemetry)

    # 1. Query for exposure_score > 50
    res = engine.execute_hunt_query(
        dsl_query="FIND assets WHERE exposure_score > 50",
        tenant_id="tenant_dsl_test",
        max_results=10,
    )
    assert len(res) == 2
    assert all(r["exposure_score"] > 50 for r in res)
