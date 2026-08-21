"""Threat Actor Attribution Test Suite (Phase 4.0 Part 5 — Section 94).

Implements Tests 19 to 20:
- Test 19: Infrastructure resembles actor -> Association only, NOT confirmed attribution.
- Test 20: Authoritative threat intelligence explicitly attributes infrastructure -> Attribution with source.
"""

import pytest
from app.schemas.intelligence_graph_models import ThreatActorAssociationDTO


class TestThreatActorAttributionSuite:
    def test_19_infrastructure_resemblance_is_association_only(self):
        assoc = ThreatActorAssociationDTO(
            association_id="taa_01",
            actor_name="Lazarus Group",
            campaign_id="camp_01",
            confidence="LOW",
            attribution_type="INFRASTRUCTURE_ASSOCIATION",
            attribution_status="UNCONFIRMED",
            evidence="Shared C2 HTTP header pattern",
        )
        assert assoc.attribution_type == "INFRASTRUCTURE_ASSOCIATION"
        assert assoc.attribution_status == "UNCONFIRMED"

    def test_20_authoritative_threat_intel_attribution(self):
        assoc = ThreatActorAssociationDTO(
            association_id="taa_02",
            actor_name="SideCopy",
            campaign_id="camp_02",
            confidence="HIGH",
            source="CERT-In Threat Advisory TA-2026-08",
            attribution_type="EXPLICIT_SOURCE_ATTRIBUTION",
            attribution_status="CONFIRMED",
            evidence="Matching C2 domain and malware XOR decryption key",
        )
        assert assoc.attribution_type == "EXPLICIT_SOURCE_ATTRIBUTION"
        assert assoc.attribution_status == "CONFIRMED"
        assert "CERT-In" in assoc.source
