"""Confidence Fusion Service for Evidence Consolidation (Phase 3.9 Part 1A.25).

Fuses confidence levels across direct vs inferred evidence, independent sources, and resolution state.
Applies Confidence Ceilings for unresolved dynamic boundaries (reflection, JNI, partial dataflows, stale feeds).

Zero malware probabilities or threat scores.
"""

from typing import List, Dict, Any, Optional
from app.schemas.evidence_consolidation_models import CanonicalFindingDTO, ConfidenceFusionDTO


class ConfidenceFusionService:
    """Fuses confidence metadata across evidence sources with confidence ceiling rules."""

    def fuse_confidence(
        self,
        finding_id: str,
        evidence_confidences: List[str],
        has_unresolved_reflection: bool = False,
        has_unresolved_jni: bool = False,
        has_partial_dataflow: bool = False,
        has_stale_threat_feed: bool = False,
    ) -> ConfidenceFusionDTO:
        # Base confidence fusion
        if "VERY_HIGH" in evidence_confidences and len(evidence_confidences) >= 2:
            fused = "VERY_HIGH"
        elif "HIGH" in evidence_confidences:
            fused = "HIGH"
        else:
            fused = "MEDIUM"

        # Apply Confidence Ceiling
        ceiling_applied = False
        ceiling_reason = None

        if has_unresolved_reflection or has_unresolved_jni:
            fused = "MEDIUM"
            ceiling_applied = True
            ceiling_reason = "Capped due to unresolved dynamic invocation (Reflection / JNI) boundary."
        elif has_partial_dataflow:
            fused = "MEDIUM"
            ceiling_applied = True
            ceiling_reason = "Capped due to partially resolved dataflow path."
        elif has_stale_threat_feed:
            fused = "MEDIUM"
            ceiling_applied = True
            ceiling_reason = "Capped due to stale external threat feed match."

        return ConfidenceFusionDTO(
            fusion_id=f"fuse_{finding_id}",
            finding_id=finding_id,
            fused_confidence=fused,
            confidence_ceiling_applied=ceiling_applied,
            ceiling_reason=ceiling_reason,
        )
