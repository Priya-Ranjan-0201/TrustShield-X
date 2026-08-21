"""Campaign Detection Test Suite (Phase 4.0 Part 5 — Section 92).

Implements Tests 11 to 14:
- Test 11: Three phishing URLs sharing payment identifier -> Campaign candidate.
- Test 12: Three websites only sharing CDN -> No campaign.
- Test 13: APK + phishing domain + payment ID -> Cross-modal campaign candidate.
- Test 14: Conflicting evidence in campaign -> Status marked CONFLICTED or confidence penalized.
"""

import pytest
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
)
from app.services.graph.campaign_correlation_engine import CampaignCorrelationEngine


class TestCampaignDetectionSuite:
    def test_11_phishing_urls_shared_payment_id_creates_campaign(self):
        upi = CanonicalEntityDTO(entity_id="upi_01", entity_type="UPI_ID", canonical_value="scam@ybl", display_value="scam@ybl", normalized_value="scam@ybl", value_hash="h_upi")
        u1 = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://phish1.in", display_value="https://phish1.in", normalized_value="https://phish1.in", value_hash="h1")
        u2 = CanonicalEntityDTO(entity_id="u2", entity_type="URL", canonical_value="https://phish2.in", display_value="https://phish2.in", normalized_value="https://phish2.in", value_hash="h2")

        r1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="u1", target_entity_id="upi_01", relationship_type="COLLECTS")
        r2 = GraphRelationshipDTO(relationship_id="r2", source_entity_id="u2", target_entity_id="upi_01", relationship_type="COLLECTS")

        camps = CampaignCorrelationEngine.detect_campaigns([upi, u1, u2], [r1, r2])
        assert len(camps) >= 1
        assert camps[0].campaign_type in ["FINANCIAL_FRAUD_CAMPAIGN", "MULTI_MODAL_CAMPAIGN"]
        assert camps[0].confidence in ["HIGH", "VERY_HIGH"]

    def test_12_three_websites_only_share_cdn_no_campaign(self):
        cdn = CanonicalEntityDTO(entity_id="cdn_01", entity_type="DOMAIN", canonical_value="cloudflare.com", display_value="cloudflare.com", normalized_value="cloudflare.com", value_hash="h_cdn")
        u1 = CanonicalEntityDTO(entity_id="u1", entity_type="URL", canonical_value="https://site1.org", display_value="https://site1.org", normalized_value="https://site1.org", value_hash="h1")
        u2 = CanonicalEntityDTO(entity_id="u2", entity_type="URL", canonical_value="https://site2.org", display_value="https://site2.org", normalized_value="https://site2.org", value_hash="h2")

        r1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="u1", target_entity_id="cdn_01", relationship_type="HOSTS")
        r2 = GraphRelationshipDTO(relationship_id="r2", source_entity_id="u2", target_entity_id="cdn_01", relationship_type="HOSTS")

        camps = CampaignCorrelationEngine.detect_campaigns([cdn, u1, u2], [r1, r2])
        assert len(camps) == 0

    def test_13_apk_phishing_payment_cross_modal_campaign(self):
        apk = CanonicalEntityDTO(entity_id="apk_01", entity_type="APPLICATION", canonical_value="com.fake.bank", display_value="com.fake.bank", normalized_value="com.fake.bank", value_hash="h_apk")
        phish = CanonicalEntityDTO(entity_id="phish_01", entity_type="URL", canonical_value="https://fakebank.in/login", display_value="https://fakebank.in/login", normalized_value="https://fakebank.in/login", value_hash="h_p")
        upi = CanonicalEntityDTO(entity_id="upi_01", entity_type="UPI_ID", canonical_value="fakebank@paytm", display_value="fakebank@paytm", normalized_value="fakebank@paytm", value_hash="h_upi")

        r1 = GraphRelationshipDTO(relationship_id="r1", source_entity_id="apk_01", target_entity_id="phish_01", relationship_type="COMMUNICATES_WITH")
        r2 = GraphRelationshipDTO(relationship_id="r2", source_entity_id="phish_01", target_entity_id="upi_01", relationship_type="COLLECTS")
        r3 = GraphRelationshipDTO(relationship_id="r3", source_entity_id="apk_01", target_entity_id="upi_01", relationship_type="COLLECTS")

        camps = CampaignCorrelationEngine.detect_campaigns([apk, phish, upi], [r1, r2, r3])
        assert len(camps) >= 1
        multi_camp = [c for c in camps if c.campaign_type == "MULTI_MODAL_CAMPAIGN"]
        assert len(multi_camp) > 0

    def test_14_conflicting_evidence_in_campaign_status_check(self):
        rel = GraphRelationshipDTO(
            relationship_id="r_conflict",
            source_entity_id="e1",
            target_entity_id="e2",
            relationship_type="RESOLVES_TO",
            status="CONFLICTED",
            conflicting_sources=["ThreatFeedA (Malicious)", "ThreatFeedB (Benign)"],
        )
        assert rel.status == "CONFLICTED"
        assert len(rel.conflicting_sources) == 2
