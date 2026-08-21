"""
TruthShield X — Response Plan Engine

Generates multi-option response plans with safety scoring, Digital Twin
simulation linkage, and dependency-aware comparison.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    ResponsePlanDTO,
    ResponseOptionDTO,
    SafetyScoreLiteral,
    ResponsePlanStatusLiteral,
)


class ResponsePlanEngine:
    """Generates, compares, and safety-scores response plan options."""

    def __init__(self):
        self._plans: Dict[str, ResponsePlanDTO] = {}

    def generate_response_plan(
        self,
        incident_command_id: str,
        options: List[Dict[str, Any]],
    ) -> ResponsePlanDTO:
        """Generates a response plan with multiple options and safety scores."""
        plan_options: List[ResponseOptionDTO] = []

        for opt_data in options:
            option = ResponseOptionDTO(
                objective=opt_data.get("objective", ""),
                scope=opt_data.get("scope", ""),
                expected_benefit=opt_data.get("expected_benefit", ""),
                potential_collateral_impact=opt_data.get("potential_collateral_impact", "NONE"),
                dependencies=opt_data.get("dependencies", []),
                reversibility=opt_data.get("reversibility", "UNKNOWN"),
                confidence=opt_data.get("confidence", 0.5),
                required_approvals=opt_data.get("required_approvals", ["SOC_LEAD"]),
                verification_method=opt_data.get("verification_method", ""),
                risk_reduction_score=opt_data.get("risk_reduction_score", 0.0),
                blast_radius_reduction=opt_data.get("blast_radius_reduction", 0.0),
                service_disruption_score=opt_data.get("service_disruption_score", 0.0),
                execution_complexity=opt_data.get("execution_complexity", "MEDIUM"),
            )
            option.safety_score = self._calculate_safety_score(option)
            plan_options.append(option)

        plan = ResponsePlanDTO(
            incident_command_id=incident_command_id,
            options=plan_options,
        )

        self._plans[plan.plan_id] = plan
        return plan

    def _calculate_safety_score(self, option: ResponseOptionDTO) -> SafetyScoreLiteral:
        """Calculates safety score based on reversibility, confidence, collateral, and complexity."""
        if option.reversibility == "IRREVERSIBLE" and option.execution_complexity == "HIGH":
            return "BLOCKED"

        score = 0.0
        # Reversibility contributes 40%
        rev_map = {"FULLY_REVERSIBLE": 1.0, "PARTIALLY_REVERSIBLE": 0.6, "IRREVERSIBLE": 0.1, "UNKNOWN": 0.3}
        score += rev_map.get(option.reversibility, 0.3) * 0.4

        # Confidence contributes 30%
        score += option.confidence * 0.3

        # Service disruption penalty (lower is better) 20%
        score += max(0, 1.0 - option.service_disruption_score) * 0.2

        # Complexity penalty 10%
        comp_map = {"LOW": 1.0, "MEDIUM": 0.6, "HIGH": 0.2}
        score += comp_map.get(option.execution_complexity, 0.5) * 0.1

        if score >= 0.75:
            return "SAFE"
        elif score >= 0.50:
            return "REVIEW_REQUIRED"
        else:
            return "HIGH_RISK"

    def compare_options(self, plan_id: str) -> List[Dict[str, Any]]:
        """Compares response options side-by-side."""
        plan = self._plans.get(plan_id)
        if not plan:
            return []

        comparison = []
        for opt in plan.options:
            comparison.append({
                "option_id": opt.option_id,
                "objective": opt.objective,
                "risk_reduction": opt.risk_reduction_score,
                "blast_radius_reduction": opt.blast_radius_reduction,
                "service_disruption": opt.service_disruption_score,
                "reversibility": opt.reversibility,
                "confidence": opt.confidence,
                "safety_score": opt.safety_score,
                "required_approvals": opt.required_approvals,
                "execution_complexity": opt.execution_complexity,
            })

        return comparison

    def update_option_status(
        self, plan_id: str, option_id: str, status: ResponsePlanStatusLiteral
    ) -> Optional[ResponseOptionDTO]:
        """Updates the status of a response option."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None

        for opt in plan.options:
            if opt.option_id == option_id:
                opt.status = status
                return opt
        return None

    def attach_simulation_result(
        self, plan_id: str, option_id: str, simulation_result: Dict[str, Any]
    ) -> Optional[ResponseOptionDTO]:
        """Links Digital Twin simulation results to a response option."""
        plan = self._plans.get(plan_id)
        if not plan:
            return None

        for opt in plan.options:
            if opt.option_id == option_id:
                opt.simulation_result = simulation_result
                opt.status = "SIMULATING"
                return opt
        return None
