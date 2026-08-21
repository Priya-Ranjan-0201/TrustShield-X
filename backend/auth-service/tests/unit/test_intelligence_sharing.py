import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_intelligence_sharing_classification():
    engine = CollaborativeDefenseEngine()
    contrib = engine.contribute_intelligence(
        tenant_id="tenant_1",
        contributor="usr_lead",
        raw_intelligence="C2 indicator 198.51.100.42",
        classification="PARTNER",
    )

    assert contrib.classification == "PARTNER"
    assert contrib.tenant_id == "tenant_1"
