import pytest
from app.services.knowledge_fabric.security_hypothesis_engine import SecurityHypothesisEngine


def test_hypothesis_engine_competing_hypotheses():
    engine = SecurityHypothesisEngine()
    hypotheses = engine.list_hypotheses()

    assert len(hypotheses) >= 2
    assert hypotheses[0].rank == 1
    assert hypotheses[1].rank == 2
