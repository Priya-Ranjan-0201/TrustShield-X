import pytest
from app.services.ai_governance.ai_tenant_privacy_engine import AITenantPrivacyEngine

def test_ai_tenant_isolation_filtering():
    engine = AITenantPrivacyEngine()
    results = [
        {"doc_id": "d1", "tenant_id": "tenant_a"},
        {"doc_id": "d2", "tenant_id": "tenant_b"},
    ]
    filtered = engine.filter_cross_tenant_vectors(results, "tenant_a")
    assert len(filtered) == 1
    assert filtered[0]["tenant_id"] == "tenant_a"
