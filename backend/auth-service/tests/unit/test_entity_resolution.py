import pytest
from app.services.global_intelligence.entity_resolution_engine import EntityResolutionEngine

def test_threat_entity_resolution():
    engine = EntityResolutionEngine()
    res = engine.resolve_entity("DarkStorm Operator", ["DarkStorm APT", "Storm-1044"])
    assert res["canonical_name"] == "DarkStorm Cyber Threat Cluster"
    assert res["confidence_score"] >= 0.95
