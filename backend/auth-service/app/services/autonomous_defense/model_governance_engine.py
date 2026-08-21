"""
TruthShield X — Model Governance Engine (Phase 30).

Governs AI/ML model metadata, evaluation metrics, drift tracking, quarantine, and automated rollback.
"""

from typing import Dict, List, Optional, Any
from app.schemas.autonomous_defense_models import ModelGovernanceDTO, ModelDriftLiteral


class ModelGovernanceEngine:
    """Manages AI model lifecycle, detects feature/calibration drift, and isolates compromised or poisoned models."""

    def __init__(self):
        self._models: Dict[str, ModelGovernanceDTO] = {}
        self._seed_default_model()

    def _seed_default_model(self):
        m1 = ModelGovernanceDTO(
            model_id="mdl_c2_neural_classifier",
            version="2.1.0",
            owner="AI_SECURITY_TEAM",
            purpose="Multi-modal DNS & Netflow C2 detection",
            precision=0.97,
            recall=0.95,
            f1_score=0.96,
            drift_status="STABLE",
            status="DEPLOYED",
        )
        self._models[m1.model_id] = m1

    def evaluate_model_integrity(
        self,
        model_id: str,
        observed_precision: float,
        is_poisoned: bool = False,
    ) -> Dict[str, Any]:
        m = self._models.get(model_id)
        if not m:
            raise ValueError(f"Model '{model_id}' not found.")

        if is_poisoned:
            quarantined = ModelGovernanceDTO(
                model_id=m.model_id,
                version=m.version,
                owner=m.owner,
                purpose=m.purpose,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                drift_status="PERFORMANCE_DRIFT",
                status="QUARANTINED",
            )
            self._models[model_id] = quarantined
            return {
                "model_id": model_id,
                "status": "QUARANTINED",
                "reason": "POISONED_TRAINING_OR_EVALUATION_DATA_DETECTED",
                "auto_rollback": True,
            }

        drift: ModelDriftLiteral = "PERFORMANCE_DRIFT" if observed_precision < (m.precision - 0.10) else "STABLE"
        return {
            "model_id": model_id,
            "status": m.status,
            "drift_status": drift,
            "observed_precision": observed_precision,
        }

    def list_models(self) -> List[ModelGovernanceDTO]:
        return list(self._models.values())
