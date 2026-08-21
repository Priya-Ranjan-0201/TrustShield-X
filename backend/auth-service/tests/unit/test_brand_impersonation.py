import pytest
from app.services.exposure.brand_impersonation_engine import BrandImpersonationMonitoringEngine


def test_brand_impersonation_detection():
    engine = BrandImpersonationMonitoringEngine()

    # 1. Typosquat domain
    finding_domain = engine.evaluate_suspect_identifier(
        target_brand="truthshield",
        suspect_identifier="truthshie1d-security.com",
        identifier_type="DOMAIN",
        tenant_id="tenant_imp",
    )
    assert finding_domain is not None
    assert finding_domain.risk_score >= 60.0

    # 2. Phishing keyword brand domain
    finding_phish = engine.evaluate_suspect_identifier(
        target_brand="hdfc",
        suspect_identifier="hdfc-kyc-verify-portal.net",
        identifier_type="DOMAIN",
        tenant_id="tenant_imp",
    )
    assert finding_phish is not None
    assert finding_phish.risk_score >= 80.0
    assert finding_phish.confidence >= 0.90
