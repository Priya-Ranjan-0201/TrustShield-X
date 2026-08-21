import pytest
from app.services.threat_intelligence_fusion.intelligence_source_registry import IntelligenceSourceRegistry
from app.schemas.threat_intelligence_fusion_models import IntelligenceSourceDTO

def test_intelligence_source_registration_and_listing():
    registry = IntelligenceSourceRegistry()
    sources = registry.list_sources()
    assert len(sources) >= 3
    
    new_src = IntelligenceSourceDTO(
        source_id="src_custom_partner",
        source_name="Partner Threat Feed",
        source_type="PARTNER",
        provider="PartnerCorp",
        reliability="B",
        approval_status="APPROVED"
    )
    registered = registry.register_source(new_src)
    assert registered.source_id == "src_custom_partner"
    assert registry.get_source("src_custom_partner") is not None
