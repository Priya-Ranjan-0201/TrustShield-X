"""
TruthShield X — Simulation Calibration Engine (Phase 26).

Compares simulation predictions with post-incident observations to calculate error, bias, and calibration scores.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.digital_twin_lab_models import SimulationCalibrationRecordDTO, CalibrationErrorLiteral


class SimulationCalibrationEngine:
    """Calibrates digital twin models by benchmarking predictions against real incident outcomes."""

    def __init__(self):
        self._records: Dict[str, SimulationCalibrationRecordDTO] = {}
        self._seed_default_calibration()

    def _seed_default_calibration(self):
        r1 = SimulationCalibrationRecordDTO(
            calibration_id="calib_drill_2026_01",
            scenario_id="scen_phishing_lateral_movement",
            predicted_outcome={"containment_time_seconds": 45.0, "affected_assets": 3},
            actual_outcome={"containment_time_seconds": 42.0, "affected_assets": 3},
            error_classification="CORRECT",
            bias_metric=0.02,
            calibration_score=0.96,
        )
        self._records[r1.calibration_id] = r1

    def record_calibration(
        self,
        scenario_id: str,
        predicted_outcome: Dict[str, Any],
        actual_outcome: Dict[str, Any],
    ) -> SimulationCalibrationRecordDTO:
        pred_time = predicted_outcome.get("containment_time_seconds", 45.0)
        actual_time = actual_outcome.get("containment_time_seconds", 42.0)

        delta = abs(pred_time - actual_time)
        if delta <= 5.0:
            error_class: CalibrationErrorLiteral = "CORRECT"
        elif pred_time < actual_time:
            error_class = "UNDERPREDICTION"
        else:
            error_class = "OVERPREDICTION"

        calibration_score = round(max(0.0, 1.0 - (delta / 100.0)), 2)

        dto = SimulationCalibrationRecordDTO(
            scenario_id=scenario_id,
            predicted_outcome=predicted_outcome,
            actual_outcome=actual_outcome,
            error_classification=error_class,
            bias_metric=round((pred_time - actual_time) / actual_time, 3),
            calibration_score=calibration_score,
            calibrated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._records[dto.calibration_id] = dto
        return dto

    def get_calibration(self, calibration_id: str) -> Optional[SimulationCalibrationRecordDTO]:
        return self._records.get(calibration_id)

    def list_calibrations(self) -> List[SimulationCalibrationRecordDTO]:
        return list(self._records.values())
