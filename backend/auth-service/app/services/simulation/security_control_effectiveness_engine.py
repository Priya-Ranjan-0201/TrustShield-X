"""
TruthShield X — Security Control Effectiveness & Gap Detection Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.simulation_models import SecurityControlDTO


class SecurityControlEffectivenessEngine:
    """Simulates security control coverage, compares modeled vs observed effectiveness, and detects defensive gaps."""

    def evaluate_controls(
        self,
        controls: List[SecurityControlDTO],
    ) -> Dict[str, Any]:
        """Calculates aggregated defensive effectiveness across configured security controls."""
        if not controls:
            return {"overall_effectiveness": 0.0, "gaps": ["No active security controls modeled."]}

        avg_modeled = sum(c.modeled_effectiveness for c in controls) / len(controls)
        observed_list = [c.observed_effectiveness for c in controls if c.observed_effectiveness is not None]
        avg_observed = (sum(observed_list) / len(observed_list)) if observed_list else avg_modeled

        gaps = []
        for c in controls:
            if c.modeled_effectiveness < 0.70:
                gaps.append(f"Weak control coverage detected in '{c.name}' ({c.control_type}).")
            if c.state in ("DEGRADED", "DISABLED", "BYPASSED_SIMULATION"):
                gaps.append(f"Control '{c.name}' is in non-optimal state: {c.state}.")

        return {
            "overall_modeled_effectiveness": round(avg_modeled, 2),
            "overall_observed_effectiveness": round(avg_observed, 2),
            "control_gaps_detected": gaps,
            "controls_count": len(controls),
            "coverage_rating": "OPTIMAL" if avg_modeled >= 0.85 else "NEEDS_IMPROVEMENT",
        }
