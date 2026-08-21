import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.intelligence_revocation_engine import IntelligenceRevocationEngine


def test_downstream_reassessment_impact_calculated():
    engine = IntelligenceRevocationEngine()
    obj = ThreatIntelligenceObjectDTO(
        intelligence_type="IP",
        raw_indicator="198.51.100.99",
        related_campaign_ids=["gcmp_123", "gcmp_456"],
    )

    impact = engine.revoke_intelligence(
        obj,
        reason="Disputed false positive",
        correlated_alert_count=5,
        correlated_incident_count=2,
        correlated_hunt_count=3,
    )

    assert impact.reassessment_required is True
    assert impact.affected_alerts_count == 5
    assert impact.affected_incidents_count == 2
    assert impact.affected_hunts_count == 3
    assert impact.affected_campaigns_count == 2
