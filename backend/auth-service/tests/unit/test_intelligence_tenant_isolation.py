import pytest
from app.services.global_intelligence.intelligence_source_manager import IntelligenceSourceManager

def test_intelligence_tenant_isolation():
    mgr = IntelligenceSourceManager()
    mgr.register_source("Tenant B Source", "INTERNAL", tenant_scope="tenant_b")
    
    tenant_a_sources = mgr.list_sources("tenant_a")
    for s in tenant_a_sources:
        assert s.tenant_scope != "tenant_b"
