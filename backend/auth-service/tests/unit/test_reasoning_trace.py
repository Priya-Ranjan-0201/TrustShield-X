import pytest
from app.services.knowledge_fabric.security_reasoning_engine import SecurityReasoningEngine


def test_reasoning_trace_explainability_elements():
    engine = SecurityReasoningEngine()
    traces = engine.list_traces()

    assert len(traces) >= 1
    t = traces[0]

    assert len(t.supporting_evidence) >= 1
    assert len(t.relationships) >= 1
    assert len(t.assumptions) >= 1
    assert len(t.contradictions) >= 1
    assert len(t.limitations) >= 1
