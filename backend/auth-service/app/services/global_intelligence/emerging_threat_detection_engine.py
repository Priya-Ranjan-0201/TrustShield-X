"""
TruthShield X — Emerging Threat Detection Engine (Phase 27).

Detects early weak signals, unusual indicator growth, and novel TTP combinations.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone
from app.schemas.global_intelligence_models import EarlyWarningSignalDTO


class EmergingThreatDetectionEngine:
    """Surfaces weak indicators and emerging threat vectors before full campaign maturity."""

    def __init__(self):
        self._signals: Dict[str, EarlyWarningSignalDTO] = {}
        self._seed_default_signal()

    def _seed_default_signal(self):
        s1 = EarlyWarningSignalDTO(
            signal_id="ew_darkstorm_burst",
            threat_name="DarkStorm Rapid C2 Expansion",
            severity="HIGH",
            velocity_score=0.85,
            novelty_score=0.78,
            affected_assets=["ast_api_gw", "ast_auth_cluster"],
            recommended_action="Pre-position rate-limiting Sigma rules on edge API gateways and simulate in Digital Twin.",
            detected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._signals[s1.signal_id] = s1

    def detect_emerging_signal(
        self,
        threat_name: str,
        velocity_score: float,
        novelty_score: float,
        affected_assets: List[str],
        severity: str = "HIGH",
    ) -> EarlyWarningSignalDTO:
        dto = EarlyWarningSignalDTO(
            threat_name=threat_name,
            severity=severity,  # type: ignore
            velocity_score=velocity_score,
            novelty_score=novelty_score,
            affected_assets=affected_assets,
            recommended_action="Validate primary detection rules and run Digital Twin what-if simulation.",
            detected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._signals[dto.signal_id] = dto
        return dto

    def list_signals(self) -> List[EarlyWarningSignalDTO]:
        return list(self._signals.values())
