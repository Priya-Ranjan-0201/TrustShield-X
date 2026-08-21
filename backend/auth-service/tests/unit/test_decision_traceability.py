import pytest
from app.services.knowledge_fabric.decision_traceability_engine import DecisionTraceabilityEngine


def test_decision_traceability_provenance():
    engine = DecisionTraceabilityEngine()
    decisions = engine.list_decisions()

    assert len(decisions) >= 1
    d = decisions[0]
    assert d.governing_policy == "POL_SEC_AUTO_ISOLATION_CRITICAL"
    assert len(d.driving_knowledge) >= 1
    assert len(d.supporting_evidence) >= 1
    assert len(d.alternative_options) >= 1
