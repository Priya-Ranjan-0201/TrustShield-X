"""
TruthShield X — Model Registry Engine (Phase 31).

Tracks model provenance, risk classifications, approval workflows, and validates SHA-256 artifact integrity.
"""

from typing import Dict, List, Optional, Any
from app.schemas.ai_security_governance_models import ModelRegistryDTO, ModelStatusLiteral


class ModelRegistryEngine:
    """Manages AI/ML model metadata, provenance, and verifies cryptographic artifact checksums."""

    def __init__(self):
        self._models: Dict[str, ModelRegistryDTO] = {}
        self._seed_default_model()

    def _seed_default_model(self):
        m1 = ModelRegistryDTO(
            model_id="mdl_c2_neural_classifier",
            model_name="C2 Multi-Modal Detection Engine",
            version="2.1.0",
            provider="INTERNAL",
            architecture="Transformer-DeBERTa-V3",
            source="s3://truthshield-models/c2-v2.1.0.pt",
            checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            dependencies=["torch==2.6.0", "transformers==4.49.0"],
            supported_modalities=["TEXT", "NETFLOW", "DNS"],
            intended_use="High-accuracy C2 beaconing anomaly detection",
            prohibited_use="Automated destructive remediation without Four-Eyes gate",
            risk_class="HIGH",
            approval_status="APPROVED",
            deployment_status="DEPLOYED",
        )
        self._models[m1.model_id] = m1

    def verify_model_integrity(self, model_id: str, computed_checksum: str) -> Dict[str, Any]:
        m = self._models.get(model_id)
        if not m:
            raise ValueError(f"Model '{model_id}' not found.")

        if computed_checksum != m.checksum:
            return {
                "model_id": model_id,
                "status": "MODEL_INTEGRITY_VIOLATION",
                "is_verified": False,
                "reason": f"CHECKSUM_MISMATCH_EXPECTED_{m.checksum}_GOT_{computed_checksum}",
            }

        return {
            "model_id": model_id,
            "status": "VERIFIED",
            "is_verified": True,
            "reason": "CRYPTOGRAPHIC_CHECKSUM_MATCHED",
        }

    def list_models(self) -> List[ModelRegistryDTO]:
        return list(self._models.values())

    def get_model(self, model_id: str) -> Optional[ModelRegistryDTO]:
        return self._models.get(model_id)
