"""Unit Tests — Payment, Audio, Document, and Threat Intel Correlation (Phase 4.0 Part 5 — Section 51)."""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules.payment_rules import (
    PaymentCorrelationRule,
    ThreatIntelCorrelationRule,
)


class TestPaymentAudioDocumentThreatIntelCorrelation:
    def test_phishing_url_collects_upi_identifier(self):
        url = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://phish.in/pay", display_value="https://phish.in/pay", normalized_value="https://phish.in/pay", value_hash="h1")
        upi = CanonicalEntityDTO(entity_id="up1", entity_type="UPI_ID", canonical_value="fraudster@ybl", display_value="fraudster@ybl", normalized_value="fraudster@ybl", value_hash="h2")

        res = PaymentCorrelationRule.evaluate(url, upi)
        assert res.matched is True
        assert res.relationship_type == "COLLECTS"
        assert res.confidence == "HIGH"

    def test_threat_intelligence_ioc_direct_match(self):
        dom = CanonicalEntityDTO(entity_id="d1", entity_type="DOMAIN", canonical_value="c2-server.net", display_value="c2-server.net", normalized_value="c2-server.net", value_hash="h1")
        ioc = CanonicalEntityDTO(entity_id="i1", entity_type="IOC", canonical_value="c2-server.net", display_value="c2-server.net", normalized_value="c2-server.net", value_hash="h1")

        res = ThreatIntelCorrelationRule.evaluate(dom, ioc)
        assert res.matched is True
        assert res.relationship_type == "MATCHES"
        assert res.confidence == "VERY_HIGH"
