"""Enterprise Risk Decision Engine (Phase 3.9 Part 1B).

Evaluates normalized risk score (0-100), risk band mapping, evidence sufficiency, confidence level,
and decision state determination.
"""

from typing import Dict, Any, Tuple
from app.core.risk_policy import RiskPolicy


class RiskDecisionEngine:
    """Decision Engine mapping scores to risk bands, sufficiency, and decision states."""

    def map_score_to_band(self, score: float) -> str:
        score = max(RiskPolicy.MIN_SCORE, min(RiskPolicy.MAX_SCORE, score))
        for band, (low, high) in RiskPolicy.BAND_THRESHOLDS.items():
            if low <= score <= high:
                return band
        return "CRITICAL_RISK" if score > 80.0 else "TRUSTED"

    def evaluate_decision_state(
        self,
        score: float,
        confidence_level: str,
        evidence_sufficiency: str,
        contradiction_count: int = 0,
    ) -> Tuple[str, str]:
        band = self.map_score_to_band(score)

        if contradiction_count > 0 and confidence_level in ["LOW", "VERY_LOW"]:
            return "CONFLICTED_ASSESSMENT", "ADDITIONAL_EVIDENCE_RECOMMENDED"

        if evidence_sufficiency == "INSUFFICIENT":
            return "INSUFFICIENT_EVIDENCE", "LOW_CONFIDENCE"

        return band, "ANALYSIS_COMPLETE"
