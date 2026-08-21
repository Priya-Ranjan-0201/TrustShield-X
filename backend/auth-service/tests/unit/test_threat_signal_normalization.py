import pytest
from app.services.predictive.threat_signal_normalization_service import ThreatSignalNormalizationService


def test_threat_signal_ingestion_and_normalization():
    service = ThreatSignalNormalizationService()
    sig = service.ingest_signal(
        signal_type="DOMAIN",
        source="CANONICAL_DEX_DETECTOR",
        entity_id="secure-verification-hdfc-portal.net",
        confidence=0.95,
        severity="HIGH",
        provenance={"detector": "dex_static_parser", "rule_id": "DEX_RULE_09"},
        ttl_seconds=3600,
        tenant_scope="tenant_omega",
    )
    assert sig.signal_id.startswith("sig_")
    assert sig.signal_type == "DOMAIN"
    assert sig.confidence == 0.95
    assert sig.lifecycle_state == "FIRST_SEEN"

    signals = service.get_signals_for_entity("secure-verification-hdfc-portal.net", "tenant_omega")
    assert len(signals) == 1
    assert signals[0].signal_id == sig.signal_id
