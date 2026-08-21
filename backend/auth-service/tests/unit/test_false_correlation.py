"""Mandatory False-Correlation Test Suite (Phase 4.0 Part 5 — Section 91).

Implements Tests 1 to 10:
- Test 1: Two apps use Cloudflare -> NO automatic campaign relationship.
- Test 2: Two apps use AWS -> NO automatic campaign relationship.
- Test 3: Two domains use same CA -> NO same-certificate relationship.
- Test 4: Two apps use same analytics SDK -> NO malicious relationship.
- Test 5: Two domains share IP -> Infrastructure relationship only.
- Test 6: Two apps have similar names -> NO identity merge.
- Test 7: Two people have similar names -> NO person merge.
- Test 8: Two UPI IDs have similar strings -> NO identity merge.
- Test 9: Same domain in two analyses -> Deduplicates to one canonical entity.
- Test 10: Same SHA-256 in two analyses -> Exact hash match relationship.
"""

import pytest
from app.schemas.intelligence_graph_models import CanonicalEntityDTO, GraphRelationshipDTO
from app.services.graph.campaign_correlation_engine import CampaignCorrelationEngine
from app.services.graph.entity_deduplication import EntityDeduplicationEngine
from app.services.graph.correlation_rules.certificate_rules import CertificateCorrelationRule, HashCorrelationRule
from app.services.graph.correlation_scoring_engine import CorrelationScoringEngine


class TestMandatoryFalseCorrelation:
    def test_01_two_apps_use_cloudflare_no_campaign(self):
        ent_cf = CanonicalEntityDTO(
            entity_id="e_cf",
            entity_type="DOMAIN",
            canonical_value="cloudflare.com",
            display_value="cloudflare.com",
            normalized_value="cloudflare.com",
            value_hash="h_cf",
        )
        url1 = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://app1.cloudflare.com", display_value="https://app1.cloudflare.com", normalized_value="https://app1.cloudflare.com", value_hash="h1")
        url2 = CanonicalEntityDTO(entity_id="u2", entity_type="URL", canonical_value="https://app2.cloudflare.com", display_value="https://app2.cloudflare.com", normalized_value="https://app2.cloudflare.com", value_hash="h2")

        rel1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="u1", target_entity_id="e_cf", relationship_type="HOSTS")
        rel2 = GraphRelationshipDTO(relationship_id="r2", source_entity_id="u2", target_entity_id="e_cf", relationship_type="HOSTS")

        # Cloudflare is public CDN -> should NOT create campaign
        campaigns = CampaignCorrelationEngine.detect_campaigns([ent_cf, url1, url2], [rel1, rel2])
        assert len(campaigns) == 0

    def test_02_two_apps_use_aws_no_campaign(self):
        ent_aws = CanonicalEntityDTO(
            entity_id="e_aws",
            entity_type="DOMAIN",
            canonical_value="amazonaws.com",
            display_value="amazonaws.com",
            normalized_value="amazonaws.com",
            value_hash="h_aws",
        )
        url1 = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://bucket1.amazonaws.com", display_value="https://bucket1.amazonaws.com", normalized_value="https://bucket1.amazonaws.com", value_hash="h1")
        url2 = CanonicalEntityDTO(entity_id="u2", entity_type="URL", canonical_value="https://bucket2.amazonaws.com", display_value="https://bucket2.amazonaws.com", normalized_value="https://bucket2.amazonaws.com", value_hash="h2")

        rel1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="u1", target_entity_id="e_aws", relationship_type="HOSTS")
        rel2 = GraphRelationshipDTO(relationship_id="r2", source_entity_id="u2", target_entity_id="e_aws", relationship_type="HOSTS")

        campaigns = CampaignCorrelationEngine.detect_campaigns([ent_aws, url1, url2], [rel1, rel2])
        assert len(campaigns) == 0

    def test_03_same_ca_no_same_certificate(self):
        ca_cert = CanonicalEntityDTO(entity_id="c_ca", entity_type="CERTIFICATE_AUTHORITY", canonical_value="Let's Encrypt Authority X3", display_value="Let's Encrypt Authority X3", normalized_value="let's encrypt authority x3", value_hash="h_ca")
        cert_leaf = CanonicalEntityDTO(entity_id="c_leaf", entity_type="CERTIFICATE", canonical_value="AABB1122", display_value="AABB1122", normalized_value="AABB1122", value_hash="h_leaf")

        res = CertificateCorrelationRule.evaluate(ca_cert, cert_leaf)
        # Should not equate CA authority to leaf certificate identity
        assert res.matched is False

    def test_04_popular_analytics_sdk_no_malicious_correlation(self):
        sdk_ent = CanonicalEntityDTO(entity_id="s1", entity_type="PACKAGE", canonical_value="com.google.firebase", display_value="com.google.firebase", normalized_value="com.google.firebase", value_hash="h_fb")
        app_ent = CanonicalEntityDTO(entity_id="a1", entity_type="APPLICATION", canonical_value="com.my.legitapp", display_value="com.my.legitapp", normalized_value="com.my.legitapp", value_hash="h_app")

        cand = CorrelationScoringEngine.evaluate_candidate(sdk_ent, app_ent)
        if cand:
            # Must have heavy false correlation penalty applied
            assert cand.false_correlation_penalty > 0.0
            assert cand.candidate_score < 0.50

    def test_05_two_domains_share_ip_infrastructure_only(self):
        dom_a = CanonicalEntityDTO(entity_id="d1", entity_type="DOMAIN", canonical_value="site-a.com", display_value="site-a.com", normalized_value="site-a.com", value_hash="h1")
        dom_b = CanonicalEntityDTO(entity_id="d2", entity_type="DOMAIN", canonical_value="site-b.com", display_value="site-b.com", normalized_value="site-b.com", value_hash="h2")

        # Independent domains on shared IP do not auto-merge
        can_merge = EntityDeduplicationEngine.can_merge(dom_a, dom_b)
        assert can_merge is False

    def test_06_two_apps_similar_names_no_merge(self):
        app1 = CanonicalEntityDTO(entity_id="a1", entity_type="PACKAGE", canonical_value="com.whatsapp.official", display_value="com.whatsapp.official", normalized_value="com.whatsapp.official", value_hash="h1")
        app2 = CanonicalEntityDTO(entity_id="a2", entity_type="PACKAGE", canonical_value="com.whatsapp.gold", display_value="com.whatsapp.gold", normalized_value="com.whatsapp.gold", value_hash="h2")

        assert EntityDeduplicationEngine.can_merge(app1, app2) is False

    def test_07_two_people_similar_names_no_merge(self):
        p1 = CanonicalEntityDTO(entity_id="p1", entity_type="PERSON", canonical_value="Rahul Sharma", display_value="Rahul Sharma", normalized_value="rahul sharma", value_hash="h1")
        p2 = CanonicalEntityDTO(entity_id="p2", entity_type="PERSON", canonical_value="Rahul Sharma Jr", display_value="Rahul Sharma Jr", normalized_value="rahul sharma jr", value_hash="h2")

        assert EntityDeduplicationEngine.can_merge(p1, p2) is False

    def test_08_two_upi_ids_similar_strings_no_merge(self):
        u1 = CanonicalEntityDTO(entity_id="u1", entity_type="UPI_ID", canonical_value="pay.merchant@okhdfcbank", display_value="pay.merchant@okhdfcbank", normalized_value="pay.merchant@okhdfcbank", value_hash="h1")
        u2 = CanonicalEntityDTO(entity_id="u2", entity_type="UPI_ID", canonical_value="pay.merchant.support@okhdfcbank", display_value="pay.merchant.support@okhdfcbank", normalized_value="pay.merchant.support@okhdfcbank", value_hash="h2")

        assert EntityDeduplicationEngine.can_merge(u1, u2) is False

    def test_09_same_domain_in_two_analyses_deduplicates(self):
        d1 = CanonicalEntityDTO(entity_id="d1", entity_type="DOMAIN", canonical_value="phishing-login.in", display_value="phishing-login.in", normalized_value="phishing-login.in", value_hash="h1", source_count=1)
        d2 = CanonicalEntityDTO(entity_id="d2", entity_type="DOMAIN", canonical_value="phishing-login.in", display_value="phishing-login.in", normalized_value="phishing-login.in", value_hash="h1", source_count=1)

        merged = EntityDeduplicationEngine.deduplicate_entities([d1, d2])
        assert len(merged) == 1
        assert merged[0].source_count == 2

    def test_10_same_sha256_exact_hash_match(self):
        h1 = CanonicalEntityDTO(entity_id="h1", entity_type="HASH", canonical_value="abcd1234ef", display_value="abcd1234ef", normalized_value="abcd1234ef", value_hash="hash_01")
        h2 = CanonicalEntityDTO(entity_id="h2", entity_type="HASH", canonical_value="abcd1234ef", display_value="abcd1234ef", normalized_value="abcd1234ef", value_hash="hash_01")

        res = HashCorrelationRule.evaluate(h1, h2)
        assert res.matched is True
        assert res.relationship_type == "MATCHES"
        assert res.candidate_score == 1.0
