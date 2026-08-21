import pytest
from app.services.knowledge_fabric.security_reasoning_engine import SecurityReasoningEngine


def test_incident_reasoning_trace():
    engine = SecurityReasoningEngine()
    traces = engine.list_traces()

    assert len(traces) >= 1
    assert "Checkout API" in traces[0].conclusion_statement
