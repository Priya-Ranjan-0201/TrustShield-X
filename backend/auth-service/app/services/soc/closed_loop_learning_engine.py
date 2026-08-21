"""
TruthShield X — Closed-Loop Learning Engine (Phase 21).

Extracts lessons learned, detection gaps, and control improvements from verified incident outcomes.
"""

from typing import Dict, List, Any


class ClosedLoopLearningEngine:
    """Extracts post-incident learnings and recommends policy/detection improvements."""

    def extract_lessons(
        self,
        incident_id: str,
        expected_state: str,
        actual_state: str,
        mttd_minutes: float,
    ) -> Dict[str, Any]:
        has_divergence = expected_state != actual_state
        return {
            "incident_id": incident_id,
            "detection_gap_detected": mttd_minutes > 15.0,
            "mttd_minutes": mttd_minutes,
            "divergence_from_expected": has_divergence,
            "recommended_improvements": [
                "Tighten WAF anomaly thresholds on webhook ingress",
                "Add automated verification query for security group egress",
            ],
            "human_approval_required_for_policy_update": True,
        }
