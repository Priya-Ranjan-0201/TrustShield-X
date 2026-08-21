"""Prediction Calibration & Outcome Tracking Engine (Phase 6 - Sections 20, 21).

Evaluates prediction calibration, records factual outcomes, and computes empirical Brier scores.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.predictive_threat_models import PredictionCalibrationRecordDTO


class PredictionCalibrationEngine:
    """Maintains immutable historical prediction records and measures calibration accuracy."""

    def __init__(self):
        self._predictions: Dict[str, PredictionCalibrationRecordDTO] = {}

    def record_prediction(
        self,
        prediction_text: str,
        predicted_probability: float,
    ) -> PredictionCalibrationRecordDTO:
        """Records a new forward-looking prediction."""
        pred_id = f"pred_{uuid.uuid4().hex[:12]}"
        record = PredictionCalibrationRecordDTO(
            prediction_id=pred_id,
            prediction_text=prediction_text,
            predicted_probability=min(1.0, max(0.0, predicted_probability)),
            actual_outcome=None,
            brier_score_contribution=None,
            evaluated_at=None,
        )
        self._predictions[pred_id] = record
        return record

    def evaluate_outcome(
        self,
        prediction_id: str,
        actual_outcome: str,  # OCCURRED or DID_NOT_OCCUR
    ) -> PredictionCalibrationRecordDTO:
        """Records actual observed outcome and computes Brier score penalty."""
        record = self._predictions.get(prediction_id)
        if not record:
            raise KeyError(f"Prediction '{prediction_id}' not found.")

        outcome_val = 1.0 if actual_outcome.upper() == "OCCURRED" else 0.0
        # Brier Score contribution: (p - o)^2
        brier = (record.predicted_probability - outcome_val) ** 2

        updated = PredictionCalibrationRecordDTO(
            prediction_id=record.prediction_id,
            prediction_text=record.prediction_text,
            predicted_probability=record.predicted_probability,
            actual_outcome=actual_outcome.upper(),
            brier_score_contribution=round(brier, 4),
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            created_at=record.created_at,
        )
        self._predictions[prediction_id] = updated
        return updated

    def get_average_brier_score(self) -> float:
        """Calculates mean Brier calibration score across all evaluated predictions (lower is better, 0.0 is perfect)."""
        evaluated = [p for p in self._predictions.values() if p.brier_score_contribution is not None]
        if not evaluated:
            return 0.0
        return round(sum(p.brier_score_contribution for p in evaluated) / len(evaluated), 4)

    def get_prediction(self, prediction_id: str) -> Optional[PredictionCalibrationRecordDTO]:
        """Retrieves an immutable prediction record."""
        return self._predictions.get(prediction_id)
