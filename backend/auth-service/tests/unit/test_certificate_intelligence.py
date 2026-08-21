import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_certificate_intelligence_expired():
    engine = ExternalAttackSurfaceEngine()
    cert = engine.record_certificate_intelligence(
        fingerprint="SHA256:CERT-99",
        tenant_id="t1",
        subject="CN=truthshield.io",
        issuer="Let's Encrypt",
        san_list=["truthshield.io", "*.truthshield.io"],
        valid_until="2024-01-01T00:00:00Z",
        is_expired=True
    )
    assert cert["is_expired"] is True
