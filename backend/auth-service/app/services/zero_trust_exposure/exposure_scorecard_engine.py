"""
Zero Trust & Threat Exposure Scorecard Engine (Phase 34)
========================================================
Aggregates enterprise exposure telemetry into executive-level risk scorecards,
quantifying Cyber Risk Exposure (CRX) and Zero Trust Maturity Levels.
"""

from typing import Dict, Any, List, Optional
import datetime


class ExposureScorecardEngine:
    def __init__(self):
        self._scorecards: Dict[str, Dict[str, Any]] = {}

    def generate_exposure_scorecard(
        self,
        tenant_id: str,
        identity_score: float = 85.0,
        device_score: float = 90.0,
        network_score: float = 78.0,
        workload_score: float = 82.0,
        data_score: float = 88.0,
        external_exposure_penalty: float = 5.0
    ) -> Dict[str, Any]:
        # Weighted overall Zero Trust Score
        zt_score = (
            identity_score * 0.25 +
            device_score * 0.20 +
            network_score * 0.20 +
            workload_score * 0.20 +
            data_score * 0.15
        ) - external_exposure_penalty

        overall_score = round(max(0.0, min(100.0, zt_score)), 1)

        if overall_score >= 85.0:
            maturity_level = "OPTIMAL_ZERO_TRUST"
        elif overall_score >= 70.0:
            maturity_level = "ADVANCED_ZERO_TRUST"
        elif overall_score >= 50.0:
            maturity_level = "INITIAL_ZERO_TRUST"
        else:
            maturity_level = "TRADITIONAL_PERIMETER"

        scorecard = {
            "tenant_id": tenant_id,
            "overall_zero_trust_score": overall_score,
            "zero_trust_score": overall_score,
            "maturity_level": maturity_level,
            "exposure_penalty": external_exposure_penalty,
            "pillar_breakdown": {
                "identity": identity_score,
                "device": device_score,
                "network": network_score,
                "workload": workload_score,
                "data": data_score
            },
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._scorecards[tenant_id] = scorecard
        return scorecard

    def compute_scorecard(
        self,
        tenant_id: str,
        identity_score: float = 85.0,
        device_score: float = 90.0,
        network_score: float = 78.0,
        workload_score: float = 82.0,
        data_score: float = 88.0,
        external_exposure_penalty: float = 5.0
    ) -> Dict[str, Any]:
        return self.generate_exposure_scorecard(
            tenant_id=tenant_id,
            identity_score=identity_score,
            device_score=device_score,
            network_score=network_score,
            workload_score=workload_score,
            data_score=data_score,
            external_exposure_penalty=external_exposure_penalty
        )

    def get_scorecard(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        return self._scorecards.get(tenant_id)


exposure_scorecard_engine = ExposureScorecardEngine()
