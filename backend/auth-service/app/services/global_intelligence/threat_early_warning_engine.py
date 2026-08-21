"""
TruthShield X — Threat Early Warning Engine (Phase 27).

Manages early warning alert states across INFORMATIONAL, WATCH, ELEVATED, HIGH, and CRITICAL thresholds.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
from app.schemas.global_intelligence_models import EarlyWarningSignalDTO, EarlyWarningSeverityLiteral


class ThreatEarlyWarningEngine:
    """Evaluates campaign surge velocity and triggers auditable early warning state transitions."""

    def __init__(self):
        self._warnings: Dict[str, EarlyWarningSignalDTO] = {}
        self._seed_default_warning()

    def _seed_default_warning(self):
        w1 = EarlyWarningSignalDTO(
            signal_id="ew_darkstorm_burst",
            threat_name="DarkStorm Rapid C2 Expansion",
            severity="HIGH",
            velocity_score=0.85,
            novelty_score=0.78,
            affected_assets=["ast_api_gw", "ast_auth_cluster"],
            recommended_action="Pre-position rate-limiting Sigma rules on edge API gateways and simulate in Digital Twin.",
            detected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._warnings[w1.signal_id] = w1

    def trigger_warning(
        self,
        threat_name: str,
        severity: EarlyWarningSeverityLiteral,
        velocity_score: float,
        affected_assets: List[str],
    ) -> EarlyWarningSignalDTO:
        dto = EarlyWarningSignalDTO(
            threat_name=threat_name,
            severity=severity,
            velocity_score=velocity_score,
            novelty_score=0.80,
            affected_assets=affected_assets,
            recommended_action="Initiate SOC threat hunt and Digital Twin simulation drill.",
            detected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._warnings[dto.signal_id] = dto
        return dto

    def list_warnings(self) -> List[EarlyWarningSignalDTO]:
        return list(self._warnings.values())
