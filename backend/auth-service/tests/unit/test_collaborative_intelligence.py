import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_collaborative_intelligence_contribution():
    engine = CollaborativeDefenseEngine()
    contrib = engine.contribute_intelligence(
        tenant_id="tenant_partner_01",
        contributor="usr_analyst_smith",
        raw_intelligence="Observed C2 traffic to evil-site.com using Bearer secret12345",
        classification="COMMUNITY",
    )

    assert contrib.is_redacted is True
    assert "secret12345" not in contrib.object_value
    assert "Bearer [REDACTED_SECRET]" in contrib.object_value
