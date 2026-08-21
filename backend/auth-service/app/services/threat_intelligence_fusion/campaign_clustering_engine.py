"""
TruthShield X — Campaign Clustering & Correlation Engine (Phase 33).

Correlates threat activities into campaigns using multi-factor clustering (temporal,
infrastructure, indicators, malware, TTPs) without false merges on single indicator overlaps.
"""

from typing import Dict, List, Any, Optional, Set
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fusion_models import ThreatCampaignDTO


class CampaignClusteringEngine:
    """Discovers, clusters, and reasons about multi-stage threat campaigns."""

    def __init__(self):
        self._campaigns: Dict[str, ThreatCampaignDTO] = {}
        self._seed_default_campaigns()

    def _seed_default_campaigns(self):
        cmp_darkstorm = ThreatCampaignDTO(
            campaign_id="cmp_darkstorm_apac",
            name="Operation DarkStorm APAC",
            description="Targeted credential harvesting and API key exfiltration campaign targeting APAC banking.",
            first_seen="2026-06-01T00:00:00Z",
            last_seen=datetime.now(timezone.utc).isoformat(),
            indicators=["ind_c2_darkstorm", "ind_hash_blackshadow"],
            techniques=["T1071.001", "T1059.001", "T1110.003"],
            malware=["mal_cobalt_beacon", "mal_ransom_blackshadow"],
            infrastructure=["198.51.100.42", "darkstorm-threat.com"],
            affected_sectors=["FINANCIAL_SERVICES", "CRITICAL_INFRASTRUCTURE"],
            affected_regions=["APAC", "SOUTH_ASIA"],
            related_actors=["act_apt_ember_bear"],
            confidence=0.88,
            evidence=["ev_telemetry_flow_20260714", "ev_cert_in_advisory_492"],
            status="ACTIVE",
        )
        cmp_ghostviper = ThreatCampaignDTO(
            campaign_id="cmp_ghostviper_cloud",
            name="GhostViper Cloud Infiltration",
            description="Multi-cloud IAM role assumption and metadata endpoint abuse.",
            first_seen="2026-07-10T00:00:00Z",
            last_seen=datetime.now(timezone.utc).isoformat(),
            indicators=["ind_c2_ghostviper"],
            techniques=["T1552.005", "T1078.004"],
            malware=["mal_viper_stealer"],
            infrastructure=["203.0.113.88"],
            affected_sectors=["TECHNOLOGY", "TELECOM"],
            affected_regions=["GLOBAL"],
            related_actors=["act_ghost_syndicate"],
            confidence=0.82,
            evidence=["ev_aws_guardduty_4091"],
            status="ACTIVE",
        )
        self._campaigns[cmp_darkstorm.campaign_id] = cmp_darkstorm
        self._campaigns[cmp_ghostviper.campaign_id] = cmp_ghostviper

    def get_campaign(self, campaign_id: str) -> Optional[ThreatCampaignDTO]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self, status: Optional[str] = None) -> List[ThreatCampaignDTO]:
        cmps = list(self._campaigns.values())
        if status:
            cmps = [c for c in cmps if c.status == status]
        return cmps

    def evaluate_campaign_merge_eligibility(
        self,
        campaign_a_id: str,
        campaign_b_id: str,
    ) -> Dict[str, Any]:
        """Evaluates multi-factor clustering invariants before any merge."""
        cmp_a = self._campaigns.get(campaign_a_id)
        cmp_b = self._campaigns.get(campaign_b_id)

        if not cmp_a or not cmp_b:
            return {"status": "CAMPAIGN_NOT_FOUND", "allowed": False}

        shared_indicators = set(cmp_a.indicators).intersection(set(cmp_b.indicators))
        shared_techniques = set(cmp_a.techniques).intersection(set(cmp_b.techniques))
        shared_malware = set(cmp_a.malware).intersection(set(cmp_b.malware))
        shared_infra = set(cmp_a.infrastructure).intersection(set(cmp_b.infrastructure))

        # Epistemic Invariant: NEVER merge solely on 1 shared indicator
        overlap_score = 0
        if len(shared_indicators) >= 2:
            overlap_score += 1
        if len(shared_techniques) >= 2:
            overlap_score += 1
        if len(shared_malware) >= 1:
            overlap_score += 1
        if len(shared_infra) >= 1:
            overlap_score += 1

        if len(shared_indicators) == 1 and len(shared_techniques) <= 1 and not shared_malware and not shared_infra:
            return {
                "status": "MERGE_REJECTED_SINGLE_INDICATOR_OVERLAP",
                "allowed": False,
                "shared_indicators": list(shared_indicators),
                "reason": "False attribution defense: single shared indicator is insufficient to merge campaigns.",
            }

        is_eligible = overlap_score >= 2
        return {
            "status": "MERGE_ELIGIBLE" if is_eligible else "INSUFFICIENT_CORROBORATION",
            "allowed": is_eligible,
            "overlap_score": overlap_score,
            "shared_indicators": list(shared_indicators),
            "shared_techniques": list(shared_techniques),
            "shared_malware": list(shared_malware),
        }
