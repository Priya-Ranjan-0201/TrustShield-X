"""
TruthShield X — Threat Early Warning Engine (Phase 33).

Generates real-time early warning signals from multi-source indicator spikes,
campaign accelerations, and critical asset exposures.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
from app.schemas.threat_intelligence_fusion_models import ThreatEarlyWarningDTO


class ThreatEarlyWarningEngine:
    """Early warning detection and automated defensive alerting system."""

    def __init__(self):
        self._warnings: Dict[str, ThreatEarlyWarningDTO] = {}
        self._seed_default_warnings()

    def _seed_default_warnings(self):
        warn_darkstorm = ThreatEarlyWarningDTO(
            warning_id="ew_darkstorm_surge_01",
            reason="Rapid C2 beacon frequency surge detected targeting APAC payment gateways.",
            evidence=["ev_telemetry_flow_20260714", "ev_c2_beacon_frequency_increase"],
            urgency="CRITICAL",
            affected_assets=["ast_payment_gw_01"],
            affected_sectors=["FINANCIAL_SERVICES"],
            recommended_actions=[
                "Deploy WAF rule to block HTTP /beacon patterns matching 198.51.100.42",
                "Force MFA re-authentication for all payment gateway administrative sessions",
                "Patch OAuth2 middleware to version 2.4.1",
            ],
            confidence=0.94,
        )
        self._warnings[warn_darkstorm.warning_id] = warn_darkstorm

    def generate_early_warning(
        self,
        reason: str,
        evidence: List[str],
        urgency: str = "HIGH",
        affected_assets: Optional[List[str]] = None,
        affected_sectors: Optional[List[str]] = None,
        recommended_actions: Optional[List[str]] = None,
        confidence: float = 0.90,
    ) -> ThreatEarlyWarningDTO:
        warn_id = f"ew_{hashlib.md5(f'{reason}:{urgency}'.encode()).hexdigest()[:8]}"
        dto = ThreatEarlyWarningDTO(
            warning_id=warn_id,
            reason=reason,
            evidence=evidence,
            urgency=urgency,
            affected_assets=affected_assets or [],
            affected_sectors=affected_sectors or [],
            recommended_actions=recommended_actions or [],
            confidence=confidence,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._warnings[warn_id] = dto
        return dto

    def get_warning(self, warning_id: str) -> Optional[ThreatEarlyWarningDTO]:
        return self._warnings.get(warning_id)

    def list_warnings(self, urgency: Optional[str] = None) -> List[ThreatEarlyWarningDTO]:
        warns = list(self._warnings.values())
        if urgency:
            warns = [w for w in warns if w.urgency == urgency]
        return warns
