import pytest
from app.services.global_defense.defensive_knowledge_sharing_engine import DefensiveKnowledgeSharingEngine

def test_defensive_knowledge_publication():
    engine = DefensiveKnowledgeSharingEngine()
    k = engine.publish_knowledge(
        problem="DarkStorm Token Replay",
        evidence=["HTTP 401 spike", "Authorization header entropy"],
        defensive_technique="Deploy Step-Up MFA & JWT Nonce Validation",
        validation_result="100% containment in Digital Twin",
        compatibility=["FASTAPI_GW", "KONG_INGRESS"],
    )
    assert k.problem == "DarkStorm Token Replay"
    assert len(engine.list_knowledge()) >= 2
