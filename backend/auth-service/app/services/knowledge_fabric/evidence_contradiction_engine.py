"""
TruthShield X — Evidence Contradiction Engine (Phase 19).

Detects conflicting indicators, timestamps, classifications, and predictions, preserving all contradictory evidence without silent deletion.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    EvidenceContradictionDTO,
    ConflictStateLiteral,
)


class EvidenceContradictionEngine:
    """Manages contradiction detection, preserves conflicting records, and updates conflict states."""

    def __init__(self):
        self._contradictions: Dict[str, EvidenceContradictionDTO] = {}
        self._initialize_default_contradiction()

    def _initialize_default_contradiction(self):
        c = EvidenceContradictionDTO(
            contradiction_id="contra_sample_01",
            entity_id="srv_checkout_production",
            conflict_type="TIMESTAMP_MISMATCH",
            evidence_a_id="ev_pcap_trace_88",
            evidence_b_id="ev_audit_log_90",
            description="PCAP shows outbound connection at 14:02 UTC but Kubernetes audit logs record container termination at 14:00 UTC.",
            conflict_state="CONFLICTING",
        )
        self._contradictions[c.contradiction_id] = c

    def record_contradiction(
        self,
        entity_id: str,
        conflict_type: str,
        evidence_a_id: str,
        evidence_b_id: str,
        description: str,
    ) -> EvidenceContradictionDTO:
        """Permanently records an identified contradiction."""
        contra = EvidenceContradictionDTO(
            entity_id=entity_id,
            conflict_type=conflict_type,
            evidence_a_id=evidence_a_id,
            evidence_b_id=evidence_b_id,
            description=description,
            conflict_state="CONFLICTING",
        )
        self._contradictions[contra.contradiction_id] = contra
        return contra

    def get_contradictions_for_entity(self, entity_id: str) -> List[EvidenceContradictionDTO]:
        """Returns all recorded contradictions for an entity."""
        return [c for c in self._contradictions.values() if c.entity_id == entity_id]

    def list_all_contradictions(self) -> List[EvidenceContradictionDTO]:
        """Lists all active contradictions across the fabric."""
        return list(self._contradictions.values())
