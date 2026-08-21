"""
TruthShield X — Crisis Readiness Engine

Multi-dimensional readiness scoring across detection, response, communication,
recovery, governance, control health, DR, and human readiness.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_models import CrisisReadinessScoreDTO


class CrisisReadinessEngine:
    """Calculates multi-dimensional crisis readiness scorecard."""

    def calculate_readiness(
        self,
        detection_readiness: float = 0.0,
        response_readiness: float = 0.0,
        communication_readiness: float = 0.0,
        recovery_readiness: float = 0.0,
        governance_readiness: float = 0.0,
        control_health_readiness: float = 0.0,
        dr_readiness: float = 0.0,
        human_readiness: float = 0.0,
    ) -> CrisisReadinessScoreDTO:
        """Calculates readiness score without simple averaging — uses weighted minimum."""
        dimensions = {
            "detection": detection_readiness,
            "response": response_readiness,
            "communication": communication_readiness,
            "recovery": recovery_readiness,
            "governance": governance_readiness,
            "control_health": control_health_readiness,
            "dr": dr_readiness,
            "human": human_readiness,
        }

        weights = {
            "detection": 0.15,
            "response": 0.20,
            "communication": 0.10,
            "recovery": 0.15,
            "governance": 0.10,
            "control_health": 0.10,
            "dr": 0.10,
            "human": 0.10,
        }

        # Weighted harmonic mean — penalizes low dimensions more than simple average
        weighted_sum = sum(weights[k] * dimensions[k] for k in dimensions)
        min_dimension = min(dimensions.values())

        # Overall is weighted average but capped by 1.5x the minimum dimension
        overall = min(weighted_sum, min_dimension * 1.5)
        overall = max(0.0, min(100.0, overall))

        return CrisisReadinessScoreDTO(
            detection_readiness=round(detection_readiness, 1),
            response_readiness=round(response_readiness, 1),
            communication_readiness=round(communication_readiness, 1),
            recovery_readiness=round(recovery_readiness, 1),
            governance_readiness=round(governance_readiness, 1),
            control_health_readiness=round(control_health_readiness, 1),
            dr_readiness=round(dr_readiness, 1),
            human_readiness=round(human_readiness, 1),
            overall_readiness=round(overall, 1),
        )
