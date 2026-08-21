import pytest
from app.services.predictive.threat_hunting_engine import ThreatHuntingEngine
from app.schemas.predictive_threat_models import ThreatHuntQueryDTO


def test_structured_threat_hunting():
    engine = ThreatHuntingEngine()
    engine.seed_hunt_entity("tenant_hunt", {
        "value": "secure-verification-hdfc-portal.net",
        "name": "Phishing C2",
        "certificate_hash": "cert_debug_8a4b",
        "infrastructure_id": "asn_4421",
    })

    # Direct search
    q = ThreatHuntQueryDTO(
        query_type="DIRECT_INDICATOR",
        search_term="hdfc-portal",
        tenant_id="tenant_hunt",
    )
    res = engine.execute_hunt(q)
    assert res.total_matched == 1
    assert res.results[0]["value"] == "secure-verification-hdfc-portal.net"


def test_natural_language_threat_hunt_translation():
    engine = ThreatHuntingEngine()
    # Natural language: "Show domains connected to this certificate"
    query = engine.translate_natural_language_query("Show domains connected to this certificate", "tenant_hunt")
    assert query.query_type == "CERTIFICATE_SHARING"
    assert query.tenant_id == "tenant_hunt"
    assert query.max_depth == 2
