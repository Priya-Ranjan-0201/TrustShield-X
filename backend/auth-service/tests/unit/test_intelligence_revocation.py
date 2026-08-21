import pytest
from app.services.threat_intelligence.collaborative_defense_engine import CollaborativeDefenseEngine


def test_intelligence_revocation_impact_tracking():
    engine = CollaborativeDefenseEngine()
    rev = engine.revoke_intelligence(
        object_id="tio_ind_c2_bad",
        reason="Upstream feed retracted indicator due to domain sinkholing.",
        affected_indicators=["tio_ind_c2_bad"],
        affected_detections=["det_rule_c2_bad"],
    )

    assert len(rev.affected_indicators) == 1
    assert len(rev.affected_detections) == 1
    assert len(rev.affected_incidents) == 1
    assert len(engine.list_revocations()) == 1
