import pytest
from app.schemas.threat_intelligence_fabric_models import ThreatIntelligenceObjectDTO


def test_indicator_lifecycle_states():
    obj_active = ThreatIntelligenceObjectDTO(
        object_type="URL",
        value="http://login-phish.net",
        canonical_value="http://login-phish.net",
        source_id="src_1",
        status="ACTIVE",
    )
    assert obj_active.status == "ACTIVE"

    obj_stale = ThreatIntelligenceObjectDTO(
        object_type="IP",
        value="192.0.2.1",
        canonical_value="192.0.2.1",
        source_id="src_1",
        status="STALE",
    )
    assert obj_stale.status == "STALE"
