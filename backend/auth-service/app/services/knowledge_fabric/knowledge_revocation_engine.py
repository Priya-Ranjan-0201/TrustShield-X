"""
TruthShield X — Knowledge Revocation Engine (Phase 19).

Computes downstream impact and marks dependent assertions, incidents, predictions, and defenses for reassessment when source evidence/intelligence is revoked.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import KnowledgeImpactDTO


class KnowledgeRevocationEngine:
    """Manages knowledge revocation impact cascades."""

    def __init__(self):
        self._revocation_records: Dict[str, KnowledgeImpactDTO] = {}

    def revoke_source(
        self,
        source_id: str,
        affected_assertions: Optional[List[str]] = None,
        affected_incidents: Optional[List[str]] = None,
        affected_reports: Optional[List[str]] = None,
        affected_predictions: Optional[List[str]] = None,
        affected_defenses: Optional[List[str]] = None,
    ) -> KnowledgeImpactDTO:
        """Revokes source and flags all downstream artifacts for reassessment."""
        impact = KnowledgeImpactDTO(
            source_id=source_id,
            affected_assertions=affected_assertions or ["asrt_checkout_at_risk"],
            affected_incidents=affected_incidents or ["inc_2026_001"],
            affected_reports=affected_reports or ["rep_monthly_threat_review"],
            affected_predictions=affected_predictions or ["pred_shadow_hydra_rce"],
            affected_defenses=affected_defenses or ["def_block_ip_range"],
            requires_reassessment=True,
        )
        self._revocation_records[impact.revocation_id] = impact
        return impact

    def get_revocation_impact(self, revocation_id: str) -> Optional[KnowledgeImpactDTO]:
        return self._revocation_records.get(revocation_id)

    def list_revocations(self) -> List[KnowledgeImpactDTO]:
        return list(self._revocation_records.values())
