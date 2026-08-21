"""
TruthShield X — Threat Early Warning Engine (Phase 22).

Generates proactive threat early warnings grounded in emerging signals and local asset relevance.
"""

from typing import List, Dict, Optional
from datetime import datetime, timezone
from app.schemas.threat_intelligence_fabric_models import ThreatEarlyWarningDTO


class ThreatEarlyWarningEngine:
    """Detects emerging adversary shifts and emits early warning signals."""

    def __init__(self):
        self._warnings: Dict[str, ThreatEarlyWarningDTO] = {}
        self._seed_default_warnings()

    def _seed_default_warnings(self):
        w1 = ThreatEarlyWarningDTO(
            warning_id="warn_zeroday_edge",
            threat_title="Emerging Exploit Surge on Enterprise Edge Gateways",
            severity="CRITICAL",
            confidence=0.91,
            local_relevance_score=88.5,
            affected_assets=["srv_vpn_gateway_01", "srv_edge_ingress"],
            early_warning_signals=[
                "Global honeypots report 400% scan increase on port 8443.",
                "Targeted ASN matches tenant ingress cloud providers.",
                "PoC exploit observed circulating in underground telemetry.",
            ],
            is_confirmed=False,
        )
        self._warnings[w1.warning_id] = w1

    def evaluate_signals(
        self,
        title: str,
        signals: List[str],
        affected_assets: List[str],
        relevance_score: float = 80.0,
    ) -> ThreatEarlyWarningDTO:
        dto = ThreatEarlyWarningDTO(
            threat_title=title,
            severity="HIGH" if relevance_score > 75.0 else "MEDIUM",
            confidence=0.86,
            local_relevance_score=relevance_score,
            affected_assets=affected_assets,
            early_warning_signals=signals,
            is_confirmed=False,
        )
        self._warnings[dto.warning_id] = dto
        return dto

    def list_early_warnings(self) -> List[ThreatEarlyWarningDTO]:
        return list(self._warnings.values())
