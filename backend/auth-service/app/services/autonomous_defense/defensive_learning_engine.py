"""
TruthShield X — Defensive Learning Engine (Phase 30).

Executes the closed-loop defensive learning pipeline:
OBSERVE -> DETECT -> INVESTIGATE -> RESPOND -> VERIFY -> MEASURE -> LEARN -> OPTIMIZE -> REVALIDATE.
"""

from typing import Dict, List, Optional, Any
from app.schemas.autonomous_defense_models import DefensiveLessonDTO, ClaimStatusLiteral, ApplicabilityLiteral


class DefensiveLearningEngine:
    """Manages verified learning pipelines preventing poisoned, fabricated, or unverified lessons."""

    def evaluate_learning_candidate(
        self,
        observation: str,
        evidence: List[str],
        action_taken: str,
        expected_outcome: str,
        actual_outcome: Optional[str],
        is_verified_by_telemetry: bool,
        confidence: float,
        has_conflicting_evidence: bool = False,
        is_simulation_only: bool = False,
        applicability: ApplicabilityLiteral = "TENANT_SPECIFIC",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        # 1. Epistemic Invariant: Simulation alone cannot become production verified fact
        if is_simulation_only:
            return {
                "status": "SIMULATED",
                "can_learn_to_production": False,
                "reason": "SIMULATION_NOT_PRODUCTION_FACT",
                "lesson": None,
            }

        # 2. Epistemic Invariant: Unverified outcomes cannot be learned
        if not is_verified_by_telemetry or actual_outcome is None:
            return {
                "status": "OUTCOME_NOT_VERIFIED",
                "can_learn_to_production": False,
                "reason": "OUTCOME_UNVERIFIED_OR_MISSING",
                "lesson": None,
            }

        # 3. Epistemic Invariant: Conflicting evidence triggers LEARNING_CONFLICT
        if has_conflicting_evidence:
            return {
                "status": "LEARNING_CONFLICT",
                "can_learn_to_production": False,
                "reason": "CONTRADICTORY_EVIDENCE_DETECTED",
                "lesson": None,
            }

        # 4. Epistemic Invariant: Insufficient confidence triggers LEARNING_NOT_SUPPORTED
        if confidence < 0.80:
            return {
                "status": "LEARNING_NOT_SUPPORTED",
                "can_learn_to_production": False,
                "reason": f"CONFIDENCE_{confidence}_BELOW_0.80_THRESHOLD",
                "lesson": None,
            }

        # Valid verified lesson
        lesson = DefensiveLessonDTO(
            threat_pattern=observation,
            environment="Production Cluster",
            recommended_action=action_taken,
            expected_gain=expected_outcome,
            evidence_count=len(evidence),
            validation_count=1,
            confidence=confidence,
            applicability=applicability,
            status="LEARNED",
            tenant_id=tenant_id,
        )

        return {
            "status": "LEARNED",
            "can_learn_to_production": True,
            "reason": "OUTCOME_VERIFIED_EVIDENCE_GROUNDED",
            "lesson": lesson,
        }
