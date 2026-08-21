import pytest
from app.services.ai_governance.secure_rag_engine import SecureRAGEngine

def test_rag_tenant_isolation_drops_foreign_data():
    engine = SecureRAGEngine()
    docs = [
        {"doc_id": "d1", "tenant_id": "foreign_tenant", "content": "Secret intel", "is_verified": True}
    ]
    res = engine.evaluate_retrieval_security("query", docs, "my_tenant")
    assert res["retrieved_count"] == 0
