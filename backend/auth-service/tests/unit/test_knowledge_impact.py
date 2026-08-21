import pytest
from app.services.knowledge_fabric.knowledge_revocation_engine import KnowledgeRevocationEngine


def test_knowledge_impact_trace_cascade():
    engine = KnowledgeRevocationEngine()
    impact = engine.revoke_source(
        source_id="ev_compromised_feed",
        affected_assertions=["asrt_1", "asrt_2"],
        affected_defenses=["def_isolate_host"],
    )

    assert len(impact.affected_assertions) == 2
    assert "def_isolate_host" in impact.affected_defenses
