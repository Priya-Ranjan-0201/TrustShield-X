import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.intelligence_privacy_engine import IntelligencePrivacyEngine


def test_privacy_transformation_anonymizes_tenant():
    engine = IntelligencePrivacyEngine()
    obj = ThreatIntelligenceObjectDTO(
        tenant_id="private_bank_tenant_99",
        intelligence_type="DOMAIN",
        raw_indicator="phishing-login-page.com",
        classification="CONFIDENTIAL",
    )

    shared_obj, record = engine.transform_for_sharing(obj, tenant_industry="FINANCIAL_SERVICES")

    assert shared_obj.tenant_id == "ANONYMIZED_FEDERATION_SOURCE"
    assert "COHORT_FINANCIAL_SERVICES" in shared_obj.anonymized_tenant_cohort
    assert "private_bank_tenant_99" not in str(shared_obj.provenance)
    assert record.is_safe_to_share is True


def test_privacy_transformation_detects_secrets():
    engine = IntelligencePrivacyEngine()
    obj = ThreatIntelligenceObjectDTO(
        tenant_id="tenant_secret_leak",
        intelligence_type="URL",
        raw_indicator="https://evil.com/leak?api_key=AKIAIOSFODNN7EXAMPLE",
    )

    _, record = engine.transform_for_sharing(obj)
    assert len(record.detected_secrets) > 0
    assert record.is_safe_to_share is False
