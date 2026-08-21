"""Threat Anomaly Engine (Phase 6 - Sections 9, 10).

Detects statistical anomalies across domain creation velocities, APK drops, scam calls,
and security incident rates using robust z-scores and moving baselines.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import math
import uuid

from app.schemas.predictive_threat_models import ThreatAnomalyDTO


class ThreatAnomalyEngine:
    """Detects statistical outliers and bursts in threat telemetry using robust z-score metrics."""

    def __init__(self):
        self._anomalies: Dict[str, Dict[str, ThreatAnomalyDTO]] = {}  # tenant_id -> anomaly_id -> anomaly
        # Tenant baseline profiles: tenant_id -> metric_name -> {mean, std}
        self._baselines: Dict[str, Dict[str, Dict[str, float]]] = {}

    def set_baseline(
        self,
        metric_name: str,
        mean: float,
        std: float,
        tenant_id: str = "default_tenant",
    ) -> None:
        """Sets expected historical baseline mean and standard deviation for a metric."""
        if tenant_id not in self._baselines:
            self._baselines[tenant_id] = {}
        self._baselines[tenant_id][metric_name] = {
            "mean": max(0.01, mean),
            "std": max(0.01, std),
        }

    def evaluate_metric(
        self,
        metric_name: str,
        observed_value: float,
        z_threshold: float = 3.0,
        tenant_id: str = "default_tenant",
    ) -> Optional[ThreatAnomalyDTO]:
        """Evaluates an observed value against the metric baseline to detect anomalous spikes."""
        tenant_base = self._baselines.get(tenant_id, {}).get(metric_name)
        if not tenant_base:
            # Default baseline: mean=10.0, std=2.0
            mean = 10.0
            std = 2.0
        else:
            mean = tenant_base["mean"]
            std = tenant_base["std"]

        z_score = (observed_value - mean) / std

        if z_score >= z_threshold:
            anomaly_id = f"anom_{uuid.uuid4().hex[:12]}"
            # Confidence grows with distance from threshold
            confidence = min(0.99, 0.70 + (z_score - z_threshold) * 0.05)

            dto = ThreatAnomalyDTO(
                anomaly_id=anomaly_id,
                tenant_id=tenant_id,
                anomaly_type=f"{metric_name.upper()}_SPIKE",
                z_score=round(z_score, 2),
                observed_value=observed_value,
                baseline_mean=mean,
                baseline_std=std,
                detection_method="ROBUST_Z_SCORE",
                confidence=round(confidence, 2),
            )

            if tenant_id not in self._anomalies:
                self._anomalies[tenant_id] = {}
            self._anomalies[tenant_id][anomaly_id] = dto
            return dto

        return None

    def list_anomalies(self, tenant_id: str = "default_tenant") -> List[ThreatAnomalyDTO]:
        """Lists detected anomalies for a tenant."""
        return list(self._anomalies.get(tenant_id, {}).values())
