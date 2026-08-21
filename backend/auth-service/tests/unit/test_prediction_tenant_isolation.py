import pytest
from app.services.predictive.threat_signal_normalization_service import ThreatSignalNormalizationService
from app.services.predictive.threat_hunting_engine import ThreatHuntingEngine
from app.schemas.predictive_threat_models import ThreatHuntQueryDTO


def test_threat_signal_tenant_isolation():
    service = ThreatSignalNormalizationService()
    sig_alpha = service.ingest_signal(
        signal_type="DOMAIN",
        source="FEED",
        entity_id="domain-tenant-alpha.com",
        tenant_scope="tenant_alpha",
    )

    # Tenant Alpha can access signal
    sigs_alpha = service.get_signals_for_entity("domain-tenant-alpha.com", "tenant_alpha")
    assert len(sigs_alpha) == 1

    # Tenant Beta CANNOT access Tenant Alpha's signal
    sigs_beta = service.get_signals_for_entity("domain-tenant-alpha.com", "tenant_beta")
    assert len(sigs_beta) == 0


def test_threat_hunt_tenant_isolation():
    engine = ThreatHuntingEngine()
    engine.seed_hunt_entity("tenant_alpha", {
        "value": "confidential-tenant-a-domain.com",
        "name": "Secret Threat",
    })

    # Hunt under Tenant Beta returns 0 matches for Tenant Alpha's data
    q_beta = ThreatHuntQueryDTO(
        query_type="DIRECT_INDICATOR",
        search_term="confidential-tenant-a-domain.com",
        tenant_id="tenant_beta",
    )
    res_beta = engine.execute_hunt(q_beta)
    assert res_beta.total_matched == 0
