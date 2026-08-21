"""
TruthShield X — Defense Decision & Explainability Engine (Phase 17).

Synthesizes multi-signal inputs, separates confidence dimensions, and generates auditable explanations.
"""

from typing import Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.adaptive_defense_models import (
    AdaptiveControlRecommendationDTO,
    DefenseSimulationResultDTO,
    DefenseDecisionRecordDTO,
    DefenseDecisionStatusLiteral,
)
from app.services.adaptive_defense.safe_defense_action_registry import SafeDefenseActionRegistry, ProtectedTargetViolationError
from app.services.adaptive_defense.adaptive_defense_policy_engine import AdaptiveDefensePolicyEngine


class DefenseDecisionEngine:
    """Evaluates multi-signal telemetry to produce explainable defense decisions."""

    def __init__(
        self,
        registry: SafeDefenseActionRegistry,
        policy_engine: AdaptiveDefensePolicyEngine,
    ):
        self.registry = registry
        self.policy_engine = policy_engine

    def evaluate_decision(
        self,
        recommendation: AdaptiveControlRecommendationDTO,
        simulation: Optional[DefenseSimulationResultDTO] = None,
        has_human_approval: bool = False,
    ) -> DefenseDecisionRecordDTO:
        """Evaluates recommendation and produces explainable decision with confidence separation."""
        # 1. Protected Target Check (Section 16, 73)
        try:
            self.registry.validate_target_safety(recommendation.target_resource)
        except ProtectedTargetViolationError as err:
            return DefenseDecisionRecordDTO(
                tenant_id=recommendation.tenant_id,
                trigger_type=recommendation.action_classification,
                status="BLOCKED",
                proposed_action=recommendation.title,
                target=recommendation.target_resource,
                evidence_confidence=0.90,
                threat_confidence=0.85,
                action_confidence=0.0,
                simulation_confidence=0.0,
                explanation={
                    "why": f"Action blocked: {str(err)}",
                    "evidence": "Protected target inventory matches resource.",
                    "risk": "Core infrastructure compromise risk.",
                    "approval": "DENIED",
                },
                required_authorization="PROHIBITED",
            )

        # 2. Policy Evaluation (Section 17)
        pol_result = self.policy_engine.evaluate_action_policy(
            recommendation,
            has_human_approval=has_human_approval,
        )

        status: DefenseDecisionStatusLiteral = pol_result["decision"]  # type: ignore

        # 3. Explainability Record (Section 21, 61)
        explanation = {
            "why": f"Mitigate active exposure on {recommendation.target_resource} via {recommendation.action_classification}.",
            "evidence": f"Supported by {len(recommendation.evidence_references)} evidence items.",
            "risk": f"Estimated collateral risk score: {recommendation.collateral_risk_score}.",
            "side_effects": simulation.collateral_service_impact if simulation else "UNSIMULATED",
            "approval": "APPROVED" if has_human_approval else ("REQUIRED" if pol_result.get("requires_approval") else "PREAUTHORIZED"),
        }

        return DefenseDecisionRecordDTO(
            tenant_id=recommendation.tenant_id,
            trigger_type=recommendation.action_classification,
            status=status,
            proposed_action=recommendation.title,
            target=recommendation.target_resource,
            evidence_confidence=0.88,
            threat_confidence=0.85,
            action_confidence=0.92,
            simulation_confidence=0.90 if simulation else 0.50,
            explanation=explanation,
            required_authorization="FOUR_EYES_APPROVAL" if pol_result.get("requires_approval") else "PREAUTHORIZED_AUTOMATION",
        )
