import pytest
from app.services.threat_intelligence_fusion.threat_actor_intelligence_engine import ThreatActorIntelligenceEngine

def test_actor_attribution_governance_gates():
    engine = ThreatActorIntelligenceEngine()
    # Direct SUSPECTED -> VERIFIED with <3 evidence items must be blocked
    res_blocked = engine.update_attribution(
        actor_id="act_ghost_syndicate",
        new_status="VERIFIED",
        supporting_evidence=["ev_single"],
        analyst_notes="Premature attribution"
    )
    assert res_blocked["status"] == "ATTRIBUTION_TRANSITION_BLOCKED"
    
    # Valid transition to ASSESSED
    res_ok = engine.update_attribution(
        actor_id="act_ghost_syndicate",
        new_status="ASSESSED",
        supporting_evidence=["ev_cert_in_advisory_492"],
        analyst_notes="Corroborated by national advisory"
    )
    assert res_ok["status"] == "ATTRIBUTION_UPDATED"
