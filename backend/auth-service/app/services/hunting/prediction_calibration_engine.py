"""
TruthShield X — Prediction Calibration & Feedback Loop Engine
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.hunting_models import SecurityPredictionDTO


class PredictionCalibrationEngine:
    """Evaluates prediction accuracy against observed real-world outcomes and calculates calibration metrics (Brier score)."""

    def record_prediction_outcome(
        self,
        prediction: SecurityPredictionDTO,
        outcome: str,  # CORRECT, PARTIALLY_CORRECT, INCORRECT
    ) -> SecurityPredictionDTO:
        """Records the observed real-world outcome of a security prediction."""
        prediction.actual_outcome = outcome  # type: ignore
        prediction.outcome_observed_at = datetime.now(timezone.utc).isoformat()
        return prediction

    def calculate_calibration_metrics(
        self,
        predictions: List[SecurityPredictionDTO],
    ) -> Dict[str, Any]:
        """Calculates empirical prediction accuracy and mean Brier score over resolved predictions."""
        resolved = [p for p in predictions if p.actual_outcome != "UNRESOLVED"]
        if not resolved:
            return {
                "total_predictions": len(predictions),
                "resolved_count": 0,
                "accuracy": 0.0,
                "brier_score": 0.0,
                "status": "AWAITING_RESOLVED_OUTCOMES",
            }

        correct_count = sum(1 for p in resolved if p.actual_outcome in ("CORRECT", "PARTIALLY_CORRECT"))
        accuracy = correct_count / len(resolved)

        # Brier Score = (1/N) * sum((forecast - actual)^2)
        # where actual is 1.0 for CORRECT, 0.0 for INCORRECT
        brier_sum = sum(
            (p.predicted_probability - (1.0 if p.actual_outcome == "CORRECT" else 0.0)) ** 2
            for p in resolved
        )
        brier_score = brier_sum / len(resolved)

        return {
            "total_predictions": len(predictions),
            "resolved_count": len(resolved),
            "accuracy": round(accuracy, 3),
            "brier_score": round(brier_score, 4),
            "status": "CALIBRATED",
        }
