"""
TruthShield X — Alert Priority Engine (Phase 21).

Calculates dynamic, explainable alert prioritization scores.
"""

from typing import List, Dict, Any
from app.schemas.autonomous_soc_models import AlertPriorityDTO, SOCAlertNormalizedDTO


class AlertPriorityEngine:
    """Calculates prioritized scores for alerts with transparent reasoning breakdown."""

    def compute_priority(
        self,
        alert: SOCAlertNormalizedDTO,
        asset_criticality: float = 85.0,
        exposure_score: float = 70.0,
        threat_intel_confidence: float = 90.0,
        control_health_pct: float = 90.0,
    ) -> AlertPriorityDTO:
        # Base severity score
        sev_map = {"CRITICAL": 95.0, "HIGH": 80.0, "MEDIUM": 50.0, "LOW": 25.0, "INFORMATIONAL": 10.0}
        sev_score = sev_map.get(alert.severity, 50.0)

        # Weighted calculation
        p_score = (
            sev_score * 0.35 +
            asset_criticality * 0.25 +
            (alert.confidence * 100.0) * 0.15 +
            exposure_score * 0.10 +
            threat_intel_confidence * 0.10 +
            (100.0 - control_health_pct) * 0.05
        )

        reasons = [
            f"Base Severity: {alert.severity} ({sev_score:.1f} pts, 35% wt)",
            f"Target Asset Criticality: {asset_criticality:.1f}/100 (25% wt)",
            f"Detection Confidence: {alert.confidence:.2f} (15% wt)",
            f"Perimeter Exposure: {exposure_score:.1f}/100 (10% wt)",
        ]

        return AlertPriorityDTO(
            alert_id=alert.alert_id,
            priority_score=round(p_score, 2),
            severity_weight=0.35,
            asset_criticality_weight=0.25,
            exploitability_weight=0.15,
            exposure_weight=0.10,
            threat_intel_weight=0.10,
            control_health_weight=0.05,
            reasoning_breakdown=reasons,
        )
