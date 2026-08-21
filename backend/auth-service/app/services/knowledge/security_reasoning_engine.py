"""Security Reasoning Engine (Phase 7 - Sections 10-15).

Performs deterministic, evidence-grounded security reasoning, counter-evidence evaluation,
consistency checks, and precedence-based conflict resolution.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.knowledge_fabric_models import (
    ReasoningResultDTO,
    ReasoningStateLiteral,
    KnowledgeConflictDTO,
    KnowledgeObjectDTO,
)
from app.services.knowledge.knowledge_fabric_service import KnowledgeFabricService


class SecurityReasoningEngine:
    """Deterministic security reasoning engine with counter-evidence and conflict resolution."""

    def __init__(self, fabric: Optional[KnowledgeFabricService] = None):
        self.fabric = fabric or KnowledgeFabricService()
        self._conflicts: Dict[str, Dict[str, KnowledgeConflictDTO]] = {}  # tenant_id -> conflict_id -> conflict

    # -----------------------------------------------------------------------
    # Section 10, 11, 12: Structured Security Reasoning
    # -----------------------------------------------------------------------

    def evaluate_claim(
        self,
        question: str,
        target_entity_reference: str,
        supporting_evidence_ids: List[str],
        counter_evidence_ids: Optional[List[str]] = None,
        base_confidence: float = 0.85,
        tenant_id: str = "default_tenant",
    ) -> ReasoningResultDTO:
        """Evaluates a security claim against supporting and counter evidence to determine reasoning state."""
        counter_ids = counter_evidence_ids or []

        # 1. Search for additional counter-evidence if not explicitly supplied
        discovered_counter = self.search_counter_evidence(target_entity_reference, tenant_id)
        all_counter_ids = list(set(counter_ids + discovered_counter))

        # 2. Compute balanced confidence: supporting boosts confidence, counter discounts it
        supporting_weight = min(1.0, len(supporting_evidence_ids) * 0.25 + base_confidence * 0.5)
        counter_discount = len(all_counter_ids) * 0.20
        final_confidence = max(0.10, min(1.0, supporting_weight - counter_discount))

        # 3. Determine Reasoning State (Section 12)
        if len(supporting_evidence_ids) == 0 and len(all_counter_ids) == 0:
            state: ReasoningStateLiteral = "UNKNOWN"
            conclusion = f"Insufficient evidence to evaluate claim regarding '{target_entity_reference}'."
            uncertainty = "HIGH"
        elif final_confidence >= 0.90 and len(all_counter_ids) == 0:
            state = "VERIFIED"
            conclusion = f"Claim regarding '{target_entity_reference}' is verified by empirical evidence."
            uncertainty = "LOW"
        elif final_confidence >= 0.70:
            state = "STRONG_INFERENCE"
            conclusion = f"Strong inference supports claim for '{target_entity_reference}' despite minor uncertainty."
            uncertainty = "MEDIUM"
        elif final_confidence >= 0.40:
            state = "WEAK_INFERENCE"
            conclusion = f"Weak inference for '{target_entity_reference}'; corroborating counter-evidence exists."
            uncertainty = "HIGH"
        else:
            state = "UNKNOWN"
            conclusion = f"Claim for '{target_entity_reference}' is unverified or contradicted by counter-evidence."
            uncertainty = "VERY_HIGH"

        reasoning_id = f"rsn_{uuid.uuid4().hex[:12]}"
        now_iso = datetime.now(timezone.utc).isoformat()

        return ReasoningResultDTO(
            reasoning_id=reasoning_id,
            question=question,
            conclusion=conclusion,
            reasoning_state=state,
            confidence=round(final_confidence, 2),
            evidence_ids=supporting_evidence_ids,
            supporting_signals=[f"evidence_count:{len(supporting_evidence_ids)}"],
            counter_evidence_ids=all_counter_ids,
            assumptions=["Evidence sources operate within validated operational thresholds"],
            uncertainty=uncertainty,
            knowledge_timestamp=now_iso,
            engine_version="7.0.0",
        )

    # -----------------------------------------------------------------------
    # Section 13: Counter-Evidence Engine
    # -----------------------------------------------------------------------

    def search_counter_evidence(self, entity_reference: str, tenant_id: str = "default_tenant") -> List[str]:
        """Searches knowledge fabric for evidence that contradicts malicious attribution."""
        objs = self.fabric.find_objects_by_reference(entity_reference, tenant_id)
        counter_evidence_ids: List[str] = []

        for o in objs:
            # If an entity has verified benign tags or whitelisted CDN infrastructure
            prov = o.provenance
            if prov.get("whitelisted") is True or prov.get("benign_signature") is True:
                counter_evidence_ids.append(o.knowledge_object_id)
            if "valid_ev_certificate" in prov.get("tags", []):
                counter_evidence_ids.append(o.knowledge_object_id)

        return counter_evidence_ids

    # -----------------------------------------------------------------------
    # Section 14: Consistency Engine & Conflict Detection
    # -----------------------------------------------------------------------

    def detect_conflicts(
        self,
        entity_reference: str,
        claimed_verdict: str,
        supporting_confidence: float,
        tenant_id: str = "default_tenant",
    ) -> Optional[KnowledgeConflictDTO]:
        """Detects contradictions such as HIGH risk claim with LOW confidence evidence, or MALICIOUS vs BENIGN."""
        # Check rule 1: High severity claim with weak evidence confidence (< 0.50)
        if claimed_verdict.upper() in ("CRITICAL", "HIGH", "MALICIOUS") and supporting_confidence < 0.50:
            conflict_id = f"cnfl_{uuid.uuid4().hex[:12]}"
            conflict = KnowledgeConflictDTO(
                conflict_id=conflict_id,
                tenant_id=tenant_id,
                entity_or_object_id=entity_reference,
                conflict_type="CONFIDENCE_SEVERITY_MISMATCH",
                description=f"High risk verdict claimed for '{entity_reference}' but supporting evidence confidence is only {supporting_confidence}.",
                supporting_evidence_ids=[],
                contradicting_evidence_ids=[],
                resolution_status="UNRESOLVED",
            )
            if tenant_id not in self._conflicts:
                self._conflicts[tenant_id] = {}
            self._conflicts[tenant_id][conflict_id] = conflict
            return conflict

        # Check rule 2: Historical benign evidence contradicts new malicious claim
        objs = self.fabric.find_objects_by_reference(entity_reference, tenant_id)
        benign_objs = [o for o in objs if o.provenance.get("verdict") == "BENIGN" and o.confidence >= 0.85]
        if claimed_verdict.upper() == "MALICIOUS" and benign_objs:
            conflict_id = f"cnfl_{uuid.uuid4().hex[:12]}"
            conflict = KnowledgeConflictDTO(
                conflict_id=conflict_id,
                tenant_id=tenant_id,
                entity_or_object_id=entity_reference,
                conflict_type="VERDICT_CONTRADICTION",
                description=f"Malicious claim contradicts existing verified benign evidence for '{entity_reference}'.",
                supporting_evidence_ids=[],
                contradicting_evidence_ids=[b.knowledge_object_id for b in benign_objs],
                resolution_status="UNRESOLVED",
            )
            if tenant_id not in self._conflicts:
                self._conflicts[tenant_id] = {}
            self._conflicts[tenant_id][conflict_id] = conflict
            return conflict

        return None

    # -----------------------------------------------------------------------
    # Section 15: Conflict Resolution by Evidence Precedence
    # -----------------------------------------------------------------------

    def resolve_conflict_by_precedence(
        self,
        conflict_id: str,
        direct_verified: bool = True,
        is_recent: bool = True,
        source_trusted: bool = True,
        tenant_id: str = "default_tenant",
    ) -> KnowledgeConflictDTO:
        """Resolves conflict applying precedence rules (Direct Verified > Inferred, Recent > Stale, Trusted > Low-confidence)."""
        conflict = self._conflicts.get(tenant_id, {}).get(conflict_id)
        if not conflict:
            raise KeyError(f"Conflict '{conflict_id}' not found.")

        rationale_parts = []
        if direct_verified:
            rationale_parts.append("Direct verified empirical evidence favored over inference.")
        if is_recent:
            rationale_parts.append("Recent verified telemetry favored over stale historical indicators.")
        if source_trusted:
            rationale_parts.append("High-credibility canonical detector favored over untrusted telemetry.")

        rationale = " ".join(rationale_parts)

        resolved_conflict = KnowledgeConflictDTO(
            conflict_id=conflict.conflict_id,
            tenant_id=conflict.tenant_id,
            entity_or_object_id=conflict.entity_or_object_id,
            conflict_type=conflict.conflict_type,
            description=conflict.description,
            supporting_evidence_ids=conflict.supporting_evidence_ids,
            contradicting_evidence_ids=conflict.contradicting_evidence_ids,
            resolution_status="RESOLVED_PRECEDENCE",
            resolution_rationale=rationale,
            detected_at=conflict.detected_at,
        )

        self._conflicts[tenant_id][conflict_id] = resolved_conflict
        return resolved_conflict
