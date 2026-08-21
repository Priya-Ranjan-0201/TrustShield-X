import pytest
from app.services.threat_intelligence_fusion.threat_actor_intelligence_engine import ThreatActorIntelligenceEngine

def test_actor_aliases_mapping():
    engine = ThreatActorIntelligenceEngine()
    actor = engine.get_actor("act_ghost_syndicate")
    assert "CloudViper Group" in actor.aliases
