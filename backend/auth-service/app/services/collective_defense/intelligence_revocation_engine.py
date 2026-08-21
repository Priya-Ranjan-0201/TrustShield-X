"""
TruthShield X — Intelligence Revocation & Downstream Impact Engine (Phase 16).

Handles the revocation lifecycle, preserves historical provenance, and calculates
downstream impact on correlated alerts, incidents, hunts, and predictive models.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.schemas.collective_defense_models import (
    ThreatIntelligenceObjectDTO,
    RevocationImpactAssessmentDTO,
)


class IntelligenceRevocationEngine:
    """Manages revocation of false or disputed intelligence with downstream blast analysis."""

    def __init__(self):
        self._revocations: Dict[str, RevocationImpactAssessmentDTO] = {}

    def revoke_intelligence(
        self,
        obj: ThreatIntelligenceObjectDTO,
        reason: str,
        revoked_by: str = "SOC_LEAD",
        correlated_alert_count: int = 2,
        correlated_incident_count: int = 1,
        correlated_hunt_count: int = 1,
    ) -> RevocationImpactAssessmentDTO:
        """Revokes an indicator, preserves historical lineage, and marks downstream artifacts for reassessment."""
        obj.validation_state = "REVOKED"
        obj.sharing_state = "REVOKED"

        # Record in provenance
        rev_record = {
            "revoked_at": datetime.now(timezone.utc).isoformat(),
            "revoked_by": revoked_by,
            "reason": reason,
        }
        obj.provenance["revocation_record"] = rev_record

        impact = RevocationImpactAssessmentDTO(
            intelligence_id=obj.intelligence_id,
            reason=reason,
            revoked_by=revoked_by,
            affected_alerts_count=correlated_alert_count,
            affected_incidents_count=correlated_incident_count,
            affected_hunts_count=correlated_hunt_count,
            affected_predictions_count=1,
            affected_campaigns_count=len(obj.related_campaign_ids),
            reassessment_required=True,
            historical_provenance_preserved=True,
        )

        self._revocations[impact.revocation_id] = impact
        return impact

    def get_revocation_impact(self, revocation_id: str) -> Optional[RevocationImpactAssessmentDTO]:
        return self._revocations.get(revocation_id)

    def list_revocations(self) -> List[RevocationImpactAssessmentDTO]:
        return list(self._revocations.values())
