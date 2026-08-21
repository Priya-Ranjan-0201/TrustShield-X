import pytest
from app.services.ai_governance.ai_tenant_privacy_engine import AITenantPrivacyEngine

def test_vector_store_tenant_filtering():
    engine = AITenantPrivacyEngine()
    raw = [{"doc_id": "v1", "tenant_id": "tenant_x"}, {"doc_id": "v2", "tenant_id": "tenant_y"}]
    res = engine.filter_cross_tenant_vectors(raw, "tenant_x")
    assert len(res) == 1
