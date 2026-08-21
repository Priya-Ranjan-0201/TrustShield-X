"""
TruthShield X — Mission Priority Engine (Phase 29).

Calculates multi-factor operational priority (CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL) with explicit contributing rationale.
"""

from typing import Dict, Any
from app.schemas.mission_control_os_models import MissionPriorityLiteral


class MissionPriorityEngine:
    """Computes transparent, evidence-weighted operational priority scores."""

    def evaluate_priority(
        self,
        severity_score: float,        # 0.0 to 1.0
        exposure_score: float,        # 0.0 to 1.0
        has_active_exploitation: bool = False,
        has_failing_controls: bool = False,
    ) -> Dict[str, Any]:
        # Weighted aggregate
        base = (severity_score * 0.4) + (exposure_score * 0.3)
        if has_active_exploitation:
            base += 0.2
        if has_failing_controls:
            base += 0.1

        composite_score = round(min(1.0, base), 2)

        if composite_score >= 0.80:
            priority: MissionPriorityLiteral = "CRITICAL"
        elif composite_score >= 0.60:
            priority = "HIGH"
        elif composite_score >= 0.40:
            priority = "MEDIUM"
        elif composite_score >= 0.20:
            priority = "LOW"
        else:
            priority = "INFORMATIONAL"

        return {
            "composite_score": composite_score,
            "priority": priority,
            "contributing_factors": {
                "severity_weight": severity_score * 0.4,
                "exposure_weight": exposure_score * 0.3,
                "active_exploitation_boost": 0.2 if has_active_exploitation else 0.0,
                "failing_control_boost": 0.1 if has_failing_controls else 0.0,
            },
            "requires_immediate_action": priority in ["CRITICAL", "HIGH"],
        }
