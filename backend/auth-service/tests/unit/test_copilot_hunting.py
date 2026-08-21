import pytest
from app.services.copilot.threat_hunting_copilot import ThreatHuntingCopilot


def test_copilot_threat_hunting_query():
    hunter = ThreatHuntingCopilot()
    query_dto = hunter.generate_hunt_query(
        query_type="SQL",
        target_entity="srv_auth_jwt",
        hypothesis="Brute force login attempts",
    )

    assert query_dto.query_type == "SQL"
    assert query_dto.is_read_only is True
    assert query_dto.safety_status == "SAFE"
    assert "LIMIT" in query_dto.query_text
