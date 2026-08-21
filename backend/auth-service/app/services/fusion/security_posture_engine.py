"""
TruthShield X — Security Posture & Situation Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.fusion_models import (
    SecurityPostureDTO,
    SecuritySituationDTO,
    PostureTrendLiteral,
    SecurityEventDTO,
)


class SecurityPostureEngine:
    """Calculates overall digital security posture across 10 distinct operational dimensions and evaluates real-time security situations."""

    def __init__(self):
        # tenant_id -> List[SecurityPostureDTO] (history)
        self._posture_history: Dict[str, List[SecurityPostureDTO]] = {}
        # tenant_id -> List[SecuritySituationDTO]
        self._situations: Dict[str, List[SecuritySituationDTO]] = {}

    def calculate_posture(
        self,
        risk_score: float,
        trust_score: float,
        exposure_score: float,
        active_threats_count: int,
        critical_assets_count: int,
        active_campaigns_count: int,
        open_incidents_count: int,
        response_success_rate: float = 0.95,
        tenant_id: str = "default_tenant",
    ) -> SecurityPostureDTO:
        """Calculates current Security Posture Score (0-100) across 10 operational dimensions."""
        # 10 Dimensions calculation
        dim_threat_level = max(0.0, 100.0 - (active_threats_count * 8.0))
        dim_asset_exposure = max(0.0, 100.0 - exposure_score)
        dim_identity_sec = 92.0
        dim_app_sec = max(0.0, 100.0 - (risk_score * 0.8))
        dim_campaign_act = max(0.0, 100.0 - (active_campaigns_count * 15.0))
        dim_incident_load = max(0.0, 100.0 - (open_incidents_count * 10.0))
        dim_response_eff = response_success_rate * 100.0
        dim_trust_health = trust_score
        dim_predictive = max(0.0, 100.0 - (risk_score * 0.5))
        dim_governance = 95.0

        dimensions = {
            "THREAT_LEVEL": round(dim_threat_level, 1),
            "ASSET_EXPOSURE": round(dim_asset_exposure, 1),
            "IDENTITY_SECURITY": round(dim_identity_sec, 1),
            "APPLICATION_SECURITY": round(dim_app_sec, 1),
            "CAMPAIGN_ACTIVITY": round(dim_campaign_act, 1),
            "INCIDENT_LOAD": round(dim_incident_load, 1),
            "RESPONSE_EFFECTIVENESS": round(dim_response_eff, 1),
            "TRUST_HEALTH": round(dim_trust_health, 1),
            "PREDICTIVE_THREAT_LEVEL": round(dim_predictive, 1),
            "GOVERNANCE_HEALTH": round(dim_governance, 1),
        }

        # Overall composite posture score
        overall = sum(dimensions.values()) / len(dimensions)
        overall_score = round(overall, 1)

        # Detect trend against history
        history = self._posture_history.get(tenant_id, [])
        trend: PostureTrendLiteral = "stable"
        trend_exp = "Security posture is stable within operational parameters."

        if history:
            prev_score = history[-1].overall_posture_score
            delta = overall_score - prev_score
            if delta <= -15.0:
                trend = "rapidly_degrading"
                trend_exp = f"Posture rapidly degraded by {abs(delta):.1f} pts due to rising threats and exposed assets."
            elif delta <= -5.0:
                trend = "degrading"
                trend_exp = f"Posture degraded by {abs(delta):.1f} pts."
            elif delta >= 5.0:
                trend = "improving"
                trend_exp = f"Posture improved by +{delta:.1f} pts following successful threat containment."

        posture_id = f"pos_{uuid.uuid4().hex[:12]}"
        posture = SecurityPostureDTO(
            posture_id=posture_id,
            tenant_id=tenant_id,
            overall_posture_score=overall_score,
            risk_score=risk_score,
            trust_score=trust_score,
            exposure_score=exposure_score,
            trend=trend,
            trend_explanation=trend_exp,
            dimensions=dimensions,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._posture_history:
            self._posture_history[tenant_id] = []
        self._posture_history[tenant_id].append(posture)

        return posture

    def evaluate_situation(
        self,
        active_threats_count: int,
        critical_assets_count: int,
        high_risk_exposure_count: int,
        active_campaigns_count: int,
        open_incidents_count: int,
        new_anomalies_count: int = 0,
        trust_degradation_events: int = 0,
        predictive_warnings_count: int = 0,
        pending_responses_count: int = 0,
        verification_failures_count: int = 0,
        tenant_id: str = "default_tenant",
    ) -> SecuritySituationDTO:
        """Evaluates and records the real-time operational security situation."""
        if open_incidents_count >= 3 or active_campaigns_count >= 2:
            threat_level = "CRITICAL"
        elif active_threats_count >= 3 or high_risk_exposure_count >= 2:
            threat_level = "HIGH"
        elif active_threats_count >= 1:
            threat_level = "ELEVATED"
        else:
            threat_level = "NORMAL"

        summary = (
            f"Security Situation is {threat_level}: {open_incidents_count} open incident(s), "
            f"{active_campaigns_count} active campaign(s), and {critical_assets_count} critical asset(s) under observation."
        )

        situation_id = f"sit_{uuid.uuid4().hex[:12]}"
        situation = SecuritySituationDTO(
            situation_id=situation_id,
            tenant_id=tenant_id,
            active_threats_count=active_threats_count,
            critical_assets_count=critical_assets_count,
            high_risk_exposure_count=high_risk_exposure_count,
            active_campaigns_count=active_campaigns_count,
            open_incidents_count=open_incidents_count,
            new_anomalies_count=new_anomalies_count,
            trust_degradation_events=trust_degradation_events,
            predictive_warnings_count=predictive_warnings_count,
            pending_responses_count=pending_responses_count,
            verification_failures_count=verification_failures_count,
            overall_threat_level=threat_level,
            summary=summary,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._situations:
            self._situations[tenant_id] = []
        self._situations[tenant_id].append(situation)

        return situation

    def get_latest_posture(self, tenant_id: str = "default_tenant") -> Optional[SecurityPostureDTO]:
        """Retrieves the latest posture evaluation."""
        history = self._posture_history.get(tenant_id, [])
        return history[-1] if history else None

    def get_posture_history(self, tenant_id: str = "default_tenant") -> List[SecurityPostureDTO]:
        """Retrieves complete posture history."""
        return self._posture_history.get(tenant_id, [])
