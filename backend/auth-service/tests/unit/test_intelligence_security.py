import pytest
from app.schemas.collective_defense_models import ThreatIntelligenceObjectDTO
from app.services.collective_defense.intelligence_ingestion_engine import MalformedIntelligenceError, IntelligenceIngestionEngine
from app.services.collective_defense.intelligence_normalization_engine import IntelligenceNormalizationEngine
from app.services.collective_defense.federation_partner_registry import FederationPartnerRegistry


def test_malformed_indicators_rejected():
    normalizer = IntelligenceNormalizationEngine()
    registry = FederationPartnerRegistry()
    ingestion = IntelligenceIngestionEngine(normalizer, registry)

    # Invalid IP
    invalid_ip = ThreatIntelligenceObjectDTO(intelligence_type="IP", raw_indicator="999.999.999.999")
    with pytest.raises(MalformedIntelligenceError):
        ingestion.ingest_single(invalid_ip, "PARTNER_X")

    # Invalid Domain
    invalid_domain = ThreatIntelligenceObjectDTO(intelligence_type="DOMAIN", raw_indicator="invalid domain name with spaces")
    with pytest.raises(MalformedIntelligenceError):
        ingestion.ingest_single(invalid_domain, "PARTNER_X")
