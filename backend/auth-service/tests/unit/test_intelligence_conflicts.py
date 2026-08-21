import pytest
from app.services.threat_intelligence_fusion.multi_source_corroboration_engine import MultiSourceCorroborationEngine

def test_intelligence_conflict_preservation():
    engine = MultiSourceCorroborationEngine()
    conf = engine.register_conflict(
        indicator_or_entity="198.51.100.99",
        claim_a="Attributed to Actor A",
        source_a="src_a",
        claim_b="Attributed to Actor B",
        source_b="src_b"
    )
    assert conf.status == "INTELLIGENCE_CONFLICT"
    assert len(engine.list_conflicts()) >= 1
