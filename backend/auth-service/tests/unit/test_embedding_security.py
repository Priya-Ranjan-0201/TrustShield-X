import pytest
from app.services.ai_governance.secure_rag_engine import SecureRAGEngine

def test_embedding_security_evaluation():
    engine = SecureRAGEngine()
    docs = [{"doc_id": "d1", "tenant_id": "tenant_a", "content": "Clean threat intel report", "is_verified": True}]
    res = engine.evaluate_retrieval_security("DarkStorm IOC", docs, "tenant_a")
    assert res["retrieved_count"] == 1
    assert res["sanitized_documents"][0]["trust_verdict"] == "VERIFIED"
