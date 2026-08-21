import pytest
from app.services.knowledge_fabric.security_knowledge_assistant import SecurityKnowledgeAssistant


def test_rag_security_grounding_hierarchy():
    assistant = SecurityKnowledgeAssistant()
    res = assistant.answer_query("What are our blind spots?")

    assert "gap_db_owner" in res.evidence
    assert res.confidence > 0.90
    assert len(res.sources) >= 1
