import pytest
from app.services.threat_intelligence_fusion.threat_actor_intelligence_engine import ThreatActorIntelligenceEngine

def test_actor_profiling_dossier():
    engine = ThreatActorIntelligenceEngine()
    actor = engine.get_actor("act_apt_ember_bear")
    assert actor is not None
    assert "Storm-0491" in actor.aliases
    assert "T1071.001" in actor.techniques
