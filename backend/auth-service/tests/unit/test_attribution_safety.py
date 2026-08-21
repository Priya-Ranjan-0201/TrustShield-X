import pytest
from app.services.global_intelligence.entity_resolution_engine import EntityResolutionEngine

def test_attribution_safety_labeled_as_inferred():
    engine = EntityResolutionEngine()
    res = engine.resolve_entity("Unknown Actor X", [])
    assert res["claim_status"] == "INFERRED"
