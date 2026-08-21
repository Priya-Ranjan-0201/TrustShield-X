"""Unit Tests — Certificate, Domain, and URL Correlation (Phase 4.0 Part 5 — Section 51)."""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO
from app.services.graph.correlation_rules.certificate_rules import CertificateCorrelationRule
from app.services.graph.correlation_rules.domain_rules import DomainCorrelationRule, URLCorrelationRule


class TestCertificateDomainURLCorrelation:
    def test_certificate_binding_to_package(self):
        pkg = CanonicalEntityDTO(entity_id="p1", entity_type="PACKAGE", canonical_value="com.trojan.app", display_value="com.trojan.app", normalized_value="com.trojan.app", value_hash="h1")
        cert = CanonicalEntityDTO(entity_id="c1", entity_type="CERTIFICATE", canonical_value="11223344", display_value="11:22:33:44", normalized_value="11223344", value_hash="h2")

        res = CertificateCorrelationRule.evaluate(pkg, cert)
        assert res.matched is True
        assert res.relationship_type == "USES_CERTIFICATE"
        assert res.confidence == "VERY_HIGH"

    def test_subdomain_correlation_to_parent_domain(self):
        d1 = CanonicalEntityDTO(entity_id="d1", entity_type="DOMAIN", canonical_value="cdn.malicious-site.com", display_value="cdn.malicious-site.com", normalized_value="cdn.malicious-site.com", value_hash="h1")
        d2 = CanonicalEntityDTO(entity_id="d2", entity_type="DOMAIN", canonical_value="malicious-site.com", display_value="malicious-site.com", normalized_value="malicious-site.com", value_hash="h2")

        res = DomainCorrelationRule.evaluate(d1, d2)
        assert res.matched is True
        assert res.relationship_type == "RESOLVES_TO"
        assert res.confidence == "HIGH"

    def test_domain_hosting_url(self):
        url = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://phish.org/bank/login", display_value="https://phish.org/bank/login", normalized_value="https://phish.org/bank/login", value_hash="h1")
        dom = CanonicalEntityDTO(entity_id="d1", entity_type="DOMAIN", canonical_value="phish.org", display_value="phish.org", normalized_value="phish.org", value_hash="h2")

        res = URLCorrelationRule.evaluate(url, dom)
        assert res.matched is True
        assert res.relationship_type == "HOSTS"
        assert res.confidence == "VERY_HIGH"
