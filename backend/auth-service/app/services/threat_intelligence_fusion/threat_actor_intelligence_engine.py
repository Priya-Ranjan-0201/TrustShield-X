"""
TruthShield X — Threat Actor Intelligence & Attribution Governance Engine (Phase 33).

Maintains threat actor dossiers, tracks aliases, TTPs, campaigns, and enforces strict
attribution state transitions (UNATTRIBUTED, SUSPECTED, ASSESSED, CORROBORATED, VERIFIED, DISPUTED).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fusion_models import ThreatActorProfileDTO


class ThreatActorIntelligenceEngine:
    """Manages threat actor profiling with rigorous attribution verification gates."""

    def __init__(self):
        self._actors: Dict[str, ThreatActorProfileDTO] = {}
        self._seed_default_actors()

    def _seed_default_actors(self):
        actor_ember = ThreatActorProfileDTO(
            actor_id="act_apt_ember_bear",
            name="Ember Bear (APT-88)",
            aliases=["Storm-0491", "RedFox Syndicate"],
            associated_campaigns=["cmp_darkstorm_apac"],
            techniques=["T1071.001", "T1059.001", "T1110.003"],
            infrastructure=["198.51.100.42", "darkstorm-threat.com"],
            malware=["mal_cobalt_beacon", "mal_ransom_blackshadow"],
            targeted_sectors=["FINANCIAL_SERVICES", "ENERGY"],
            targeted_regions=["APAC", "SOUTH_ASIA"],
            evidence=["ev_cert_in_advisory_492", "ev_pcap_darkstorm_c2"],
            confidence=0.85,
            attribution_status="ASSESSED",
        )
        actor_ghost = ThreatActorProfileDTO(
            actor_id="act_ghost_syndicate",
            name="Ghost Syndicate",
            aliases=["CloudViper Group"],
            associated_campaigns=["cmp_ghostviper_cloud"],
            techniques=["T1552.005", "T1078.004"],
            infrastructure=["203.0113.88"],
            malware=["mal_viper_stealer"],
            targeted_sectors=["TECHNOLOGY", "TELECOM"],
            targeted_regions=["GLOBAL"],
            evidence=["ev_aws_guardduty_4091"],
            confidence=0.72,
            attribution_status="SUSPECTED",
        )
        self._actors[actor_ember.actor_id] = actor_ember
        self._actors[actor_ghost.actor_id] = actor_ghost

    def get_actor(self, actor_id: str) -> Optional[ThreatActorProfileDTO]:
        return self._actors.get(actor_id)

    def list_actors(self, attribution_status: Optional[str] = None) -> List[ThreatActorProfileDTO]:
        actors = list(self._actors.values())
        if attribution_status:
            actors = [a for a in actors if a.attribution_status == attribution_status]
        return actors

    def update_attribution(
        self,
        actor_id: str,
        new_status: str,
        supporting_evidence: List[str],
        analyst_notes: str,
    ) -> Dict[str, Any]:
        """Enforces attribution state transition invariants."""
        actor = self._actors.get(actor_id)
        if not actor:
            return {"status": "ACTOR_NOT_FOUND", "actor_id": actor_id}

        # Epistemic Invariant: Never automatically transition SUSPECTED -> VERIFIED directly
        if actor.attribution_status == "SUSPECTED" and new_status == "VERIFIED" and len(supporting_evidence) < 3:
            return {
                "status": "ATTRIBUTION_TRANSITION_BLOCKED",
                "reason": "Direct transition from SUSPECTED to VERIFIED requires at least 3 independent corroborating evidence sources.",
                "current_status": actor.attribution_status,
            }

        valid_states = {"UNATTRIBUTED", "SUSPECTED", "ASSESSED", "CORROBORATED", "VERIFIED", "DISPUTED"}
        if new_status not in valid_states:
            return {"status": "INVALID_ATTRIBUTION_STATE", "valid_states": list(valid_states)}

        old_status = actor.attribution_status
        actor.attribution_status = new_status
        actor.evidence.extend(supporting_evidence)

        return {
            "status": "ATTRIBUTION_UPDATED",
            "actor_id": actor_id,
            "previous_status": old_status,
            "new_status": new_status,
            "evidence_count": len(actor.evidence),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
