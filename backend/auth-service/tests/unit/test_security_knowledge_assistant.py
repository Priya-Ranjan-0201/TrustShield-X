import pytest
from app.services.knowledge_fabric.security_knowledge_assistant import SecurityKnowledgeAssistant


def test_security_knowledge_assistant_contract():
    assistant = SecurityKnowledgeAssistant()
    res = assistant.answer_query("Why is checkout service at risk?")

    assert res.answer != ""
    assert len(res.evidence) >= 1
    assert len(res.sources) >= 1
    assert res.confidence >= 0.85
    assert len(res.limitations) >= 1
