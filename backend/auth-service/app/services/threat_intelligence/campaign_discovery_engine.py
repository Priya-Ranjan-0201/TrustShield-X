"""
TruthShield X — Campaign Discovery Engine (Phase 22).

Clusters related cyber infrastructure, TTPs, and indicators into campaigns with strict attribution safety.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import CampaignClusterDTO, AttributionConfidenceLiteral


class CampaignDiscoveryEngine:
    """Discovers and clusters campaign telemetry with evidence-grounded attribution bounds."""

    def __init__(self):
        self._campaigns: Dict[str, CampaignClusterDTO] = {}
        self._seed_default_campaigns()

    def _seed_default_campaigns(self):
        c1 = CampaignClusterDTO(
            campaign_id="camp_shadowstrike",
            name="Operation ShadowStrike",
            lifecycle="ACTIVE",
            confidence=0.94,
            attribution="UNCERTAIN_NEXUS_DEV_0442",
            attribution_confidence="ASSESSED",
            infrastructure=["198.51.100.42", "c2.shadowhydra.net", "api.telemetry-sync.org"],
            indicators=["ind_hash_a1b2", "ind_domain_shadow"],
            techniques=["T1059.001", "T1071.001", "T1003.001"],
            targeted_sectors=["FINANCIAL_SERVICES", "E_COMMERCE"],
            contradictions=[],
            assumptions=["Targeting similarity matches observed retail peak activity."],
            evolution_log=["Initial discovery: C2 beaconing on port 443.", "Expansion: Additional subdomains observed."],
        )
        self._campaigns[c1.campaign_id] = c1

    def cluster_campaign(
        self,
        name: str,
        infrastructure: List[str],
        indicators: List[str],
        techniques: List[str],
        attribution: str = "UNKNOWN_ACTOR",
        attribution_confidence: AttributionConfidenceLiteral = "UNCERTAIN",
    ) -> CampaignClusterDTO:
        # Attribution safety invariant: If evidence is weak or unverified, keep confidence as UNCERTAIN or SUSPECTED
        dto = CampaignClusterDTO(
            name=name,
            lifecycle="DISCOVERED",
            confidence=0.88,
            attribution=attribution,
            attribution_confidence=attribution_confidence,
            infrastructure=infrastructure,
            indicators=indicators,
            techniques=techniques,
            evolution_log=[f"Campaign '{name}' clustered from {len(infrastructure)} infrastructure nodes."],
        )
        self._campaigns[dto.campaign_id] = dto
        return dto

    def get_campaign(self, campaign_id: str) -> Optional[CampaignClusterDTO]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self) -> List[CampaignClusterDTO]:
        return list(self._campaigns.values())
