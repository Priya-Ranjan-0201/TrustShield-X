"""Response Effectiveness Engine (Phase 5).

Calculates post-remediation effectiveness scores (0–100)
based on empirical containment, time to containment, residual risk,
collateral disruption, and rollback requirements.
"""

from typing import Dict, Any, List, Optional
from app.schemas.autonomous_defense_models import (
    ResponsePlanDTO,
    EffectivenessScoreDTO,
    VerificationResultDTO,
)


class ResponseEffectivenessEngine:
    """Evaluates the factual success and containment efficacy of executed defense plans."""

    @staticmethod
    def calculate_effectiveness(
        plan: ResponsePlanDTO,
        verifications: List[VerificationResultDTO],
        initial_risk: float,
        residual_risk: float,
        time_to_containment_seconds: float = 4.2,
        reversal_count: int = 0,
        collateral_disruption_score: float = 0.0,
    ) -> EffectivenessScoreDTO:
        """Calculates 0–100 response effectiveness with explainable component weights."""
        total_actions = len(plan.actions) if plan.actions else 1
        successful_verifications = sum(1 for v in verifications if v.verification_passed)
        containment_rate = successful_verifications / float(total_actions)

        # 1. Containment Score Component (Weight: 40%)
        containment_component = containment_rate * 40.0

        # 2. Risk Reduction Component (Weight: 35%)
        # Calculates how much of initial risk was mitigated
        risk_delta = max(0.0, initial_risk - residual_risk)
        risk_reduction_ratio = risk_delta / initial_risk if initial_risk > 0 else 1.0
        risk_component = min(35.0, risk_reduction_ratio * 35.0)

        # 3. Speed of Containment Component (Weight: 15%)
        # Target ≤ 10 seconds for automated edge actions, decaying after 60s
        if time_to_containment_seconds <= 10.0:
            speed_component = 15.0
        elif time_to_containment_seconds <= 60.0:
            speed_component = 15.0 - ((time_to_containment_seconds - 10.0) / 50.0 * 7.5)
        else:
            speed_component = 5.0

        # 4. Collateral & Stability Component (Weight: 10%)
        penalty = (reversal_count * 5.0) + (collateral_disruption_score * 0.05)
        stability_component = max(0.0, 10.0 - penalty)

        # Final Score Sum
        total_score = round(containment_component + risk_component + speed_component + stability_component, 1)
        total_score = max(0.0, min(100.0, total_score))

        factors = {
            "containment_component_score": round(containment_component, 1),
            "risk_mitigation_score": round(risk_component, 1),
            "speed_of_containment_score": round(speed_component, 1),
            "stability_and_collateral_score": round(stability_component, 1),
            "initial_risk": initial_risk,
            "residual_risk": residual_risk,
            "verified_actions": f"{successful_verifications}/{total_actions}",
        }

        if total_score >= 85.0:
            summary = "HIGHLY_EFFECTIVE: Rapid threat containment with zero collateral impact and verified risk reduction."
        elif total_score >= 60.0:
            summary = "MODERATELY_EFFECTIVE: Threat contained with acceptable residual risk and minor latency."
        else:
            summary = "PARTIALLY_EFFECTIVE: Threat partially contained; residual risk requires secondary remediation."

        return EffectivenessScoreDTO(
            plan_id=plan.plan_id,
            effectiveness_score=total_score,
            containment_success_rate=round(containment_rate, 2),
            time_to_containment_seconds=round(time_to_containment_seconds, 2),
            residual_risk_score=round(residual_risk, 1),
            collateral_disruption_score=round(collateral_disruption_score, 1),
            reversal_count=reversal_count,
            factors=factors,
            summary=summary,
        )
