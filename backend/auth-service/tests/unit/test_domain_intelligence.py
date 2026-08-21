import pytest
from app.services.zero_trust_exposure.external_attack_surface_engine import ExternalAttackSurfaceEngine

def test_domain_intelligence_tracking():
    engine = ExternalAttackSurfaceEngine()
    intel = engine.record_domain_intelligence(
        domain="truthshield.io",
        tenant_id="t1",
        dns_records={"A": ["203.0.113.1"], "MX": ["mail.truthshield.io"]},
        registrar="MarkMonitor",
        subdomains=["api", "auth", "soc"]
    )
    assert intel["domain"] == "truthshield.io"
    assert len(intel["subdomains"]) == 3
