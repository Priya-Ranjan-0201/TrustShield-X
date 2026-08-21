import pytest
from app.services.soc.alert_priority_engine import AlertPriorityEngine
from app.schemas.autonomous_soc_models import SOCAlertNormalizedDTO


def test_alert_priority_scoring_breakdown():
    engine = AlertPriorityEngine()
    alert = SOCAlertNormalizedDTO(source="FIREWALL", asset="srv_db", severity="CRITICAL", confidence=0.98)

    p_dto = engine.compute_priority(alert, asset_criticality=95.0, exposure_score=80.0)
    assert p_dto.priority_score > 75.0
    assert len(p_dto.reasoning_breakdown) >= 4
