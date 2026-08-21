import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.intelligence_privacy_engine import IntelligencePrivacyEngine


def test_privacy_leakage_resistance():
    engine = IntelligencePrivacyEngine()

    obj = ThreatIntelligenceObjectDTO(
        tenant_id="bank_customer_internal_tenant_77",
        intelligence_type="URL",
        raw_indicator="https://login.evil.com/phish?email=alice.smith@enterprise.org&user_id=usr_998811",
    )

    shared_obj, record = engine.transform_for_sharing(obj)

    # Verify no customer internal identifier is retained in tenant_id or provenance
    assert "bank_customer_internal_tenant_77" not in shared_obj.tenant_id
    assert "bank_customer_internal_tenant_77" not in str(shared_obj.provenance)
    assert len(record.detected_pii) > 0
