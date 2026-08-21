"""
TruthShield X — Global Early Warning & Threat Trend Engine (Phase 16).

Detects emerging multi-tenant attack waves, forecasts campaign expansion,
and issues early warning broadcasts with explicit confidence and limitation guardrails.
"""

from typing import List, Dict, Optional
from datetime import datetime, timezone
import uuid

from app.schemas.collective_defense_models import (
    GlobalEarlyWarningDTO,
    GlobalThreatRiskSignalDTO,
    ThreatTrendReportDTO,
    GlobalCampaignDetailDTO,
)


class GlobalEarlyWarningEngine:
    """Evaluates cross-tenant threat surges and broadcasts early warning alerts."""

    def __init__(self):
        self._warnings: Dict[str, GlobalEarlyWarningDTO] = {}
        self._risk_signals: List[GlobalThreatRiskSignalDTO] = []

    def evaluate_campaign_for_warning(
        self,
        campaign: GlobalCampaignDetailDTO,
        affected_sectors: Optional[List[str]] = None,
    ) -> Optional[GlobalEarlyWarningDTO]:
        """Evaluates whether an emerging campaign warrants a global early warning."""
        if not campaign.expansion_warning and campaign.confidence < 0.70:
            return None

        warning = GlobalEarlyWarningDTO(
            title=f"Global Early Warning: {campaign.name}",
            summary=f"Detected coordinated campaign across {len(campaign.modalities)} modalities with {len(campaign.indicators)} indicators.",
            confidence=campaign.confidence,
            trigger_type="MULTI_MODAL_EXPANSION" if len(campaign.modalities) >= 2 else "EMERGING_CAMPAIGN",
            evidence_references=campaign.indicators[:5],
            scope="GLOBAL_CROSS_TENANT",
            affected_sectors=affected_sectors or ["FINANCIAL", "HEALTHCARE", "ECOMMERCE"],
            limitations=[
                "Attribution unconfirmed by default",
                "Based on privacy-safe correlated telemetry",
                "Does not imply direct compromise of every tenant",
            ],
            recommended_threat_hunts=[
                f"Hunt for active connections to infrastructure: {', '.join(campaign.infrastructure_nodes[:3])}",
                "Check for suspicious multi-modal authentication spikes",
            ],
        )

        self._warnings[warning.warning_id] = warning
        return warning

    def generate_risk_signal(
        self,
        category: str,
        risk_level: str = "HIGH",
        confidence: float = 0.85,
        trend: str = "ACCELERATING",
        sectors: Optional[List[str]] = None,
    ) -> GlobalThreatRiskSignalDTO:
        """Broadcasts a global threat risk signal without falsely claiming confirmed compromise."""
        signal = GlobalThreatRiskSignalDTO(
            threat_category=category,
            risk_level=risk_level,  # type: ignore
            confidence=confidence,
            expected_trend=trend,  # type: ignore
            affected_sectors=sectors or ["FINANCIAL", "CLOUD_INFRASTRUCTURE"],
            evidence_summary=f"Aggregated surge observed in {category} indicators.",
            is_confirmed_tenant_attack=False,  # Explicit safety invariant
        )
        self._risk_signals.append(signal)
        return signal

    def generate_trend_report(self, campaigns: List[GlobalCampaignDetailDTO]) -> ThreatTrendReportDTO:
        """Computes aggregate trend report."""
        total_indicators = sum(len(c.indicators) for c in campaigns)
        growth_rate = float(len(campaigns) * 1.25)

        return ThreatTrendReportDTO(
            timeframe="LAST_30_DAYS",
            indicator_growth_rate=growth_rate,
            campaign_growth_rate=float(len(campaigns)),
            top_modalities=[
                {"modality": "VOICE_CLONE", "count": sum(1 for c in campaigns if "VOICE_CLONE" in c.modalities)},
                {"modality": "QR_PHISHING", "count": sum(1 for c in campaigns if "QR_PHISHING" in c.modalities)},
                {"modality": "MALICIOUS_APK", "count": sum(1 for c in campaigns if "MALICIOUS_APK" in c.modalities)},
            ],
            top_emerging_threats=[c.name for c in campaigns[:5]],
        )

    def list_warnings(self) -> List[GlobalEarlyWarningDTO]:
        return list(self._warnings.values())

    def list_risk_signals(self) -> List[GlobalThreatRiskSignalDTO]:
        return self._risk_signals
