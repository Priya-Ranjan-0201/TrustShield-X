"""
TruthShield X — Defense Effectiveness Scoring Engine (Phase 17).

Quantifies post-adaptation threat reduction, exposure mitigation, and service stability.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone

from app.schemas.adaptive_defense_models import DefenseEffectivenessScoreDTO


class DefenseEffectivenessEngine:
    """Measures multi-dimensional post-adaptation effectiveness and residual risk."""

    def __init__(self):
        self._scores: Dict[str, DefenseEffectivenessScoreDTO] = {}

    def calculate_effectiveness(
        self,
        tenant_id: str,
        action_id: str,
        threat_reduction: float = 85.0,
        exposure_reduction: float = 70.0,
        control_improvement: float = 90.0,
        service_stability: float = 98.0,
    ) -> DefenseEffectivenessScoreDTO:
        """Calculates multi-dimensional defense effectiveness score."""
        overall = (
            threat_reduction * 0.35
            + exposure_reduction * 0.25
            + control_improvement * 0.20
            + service_stability * 0.20
        )
        residual_risk = max(0.0, 100.0 - overall)

        score = DefenseEffectivenessScoreDTO(
            tenant_id=tenant_id,
            action_id=action_id,
            threat_reduction_score=round(threat_reduction, 1),
            exposure_reduction_score=round(exposure_reduction, 1),
            control_improvement_score=round(control_improvement, 1),
            service_stability_score=round(service_stability, 1),
            overall_effectiveness=round(overall, 2),
            residual_risk_score=round(residual_risk, 2),
        )

        self._scores[action_id] = score
        return score

    def get_score(self, action_id: str) -> Optional[DefenseEffectivenessScoreDTO]:
        return self._scores.get(action_id)

    def list_scores(self, tenant_id: str = "default_tenant") -> List[DefenseEffectivenessScoreDTO]:
        return [s for s in self._scores.values() if s.tenant_id == tenant_id]
