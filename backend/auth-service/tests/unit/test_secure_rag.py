import pytest
from app.services.ai_governance.secure_rag_engine import SecureRAGEngine

def test_secure_rag_workflow():
    engine = SecureRAGEngine()
    docs = [
        {"doc_id": "d1", "tenant_id": "tenant_a", "content": "Valid C2 signature", "is_verified": True}
    ]
    res = engine.evaluate_retrieval_security("C2 signatures", docs, "tenant_a")
    assert res["status"] == "RAG_RETRIEVAL_SECURED"
