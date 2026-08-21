"""
TruthShield X — Exposure Alert Correlation & Deduplication Engine
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.exposure_models import ExposureFindingDTO, CorrelatedExposureEventDTO


class ExposureAlertCorrelationEngine:
    """Correlates multiple exposure findings and changes into unified exposure incidents and suppresses duplicates."""

    def __init__(self, cooldown_minutes: int = 60):
        self.cooldown_minutes = cooldown_minutes
        # tenant_id -> event_id -> CorrelatedExposureEventDTO
        self._events: Dict[str, Dict[str, CorrelatedExposureEventDTO]] = {}
        # tenant_id -> deduplication_key -> last_alert_timestamp
        self._dedup_cache: Dict[str, Dict[str, str]] = {}

    def correlate_findings(
        self,
        findings: List[ExposureFindingDTO],
        tenant_id: str = "default_tenant",
    ) -> Optional[CorrelatedExposureEventDTO]:
        """Correlates a batch of findings related to shared campaigns or assets into a single unified event."""
        if not findings:
            return None

        if tenant_id not in self._events:
            self._events[tenant_id] = {}
            self._dedup_cache[tenant_id] = {}

        # Extract unique assets and campaigns
        affected_assets = list(set(f.asset_id for f in findings))
        finding_ids = [f.finding_id for f in findings]
        campaigns = list(set(c for f in findings for c in f.campaign_ids))
        primary_campaign = campaigns[0] if campaigns else None

        # Deduplication signature
        dedup_key = f"{sorted(affected_assets)}:{primary_campaign}"
        now = datetime.now(timezone.utc)

        if dedup_key in self._dedup_cache[tenant_id]:
            # Cooldown check
            last_time = datetime.fromisoformat(self._dedup_cache[tenant_id][dedup_key])
            diff_mins = (now - last_time).total_seconds() / 60.0
            if diff_mins < self.cooldown_minutes:
                # Suppressed due to active cooldown window
                return None

        self._dedup_cache[tenant_id][dedup_key] = now.isoformat()

        # Compute aggregate scores
        max_exposure = max(f.exposure_score for f in findings)
        max_risk = max(f.risk_score for f in findings)
        severities = [f.severity for f in findings]
        event_severity = "CRITICAL" if "CRITICAL" in severities else ("HIGH" if "HIGH" in severities else "MEDIUM")

        event_id = f"cexp_{uuid.uuid4().hex[:12]}"
        event = CorrelatedExposureEventDTO(
            event_id=event_id,
            tenant_id=tenant_id,
            affected_assets=affected_assets,
            finding_ids=finding_ids,
            title=f"Coordinated Exposure Event across {len(affected_assets)} Asset(s)",
            summary=f"Detected {len(findings)} related exposure change(s) linked to campaign '{primary_campaign or 'UNASSIGNED'}'.",
            severity=event_severity,
            aggregate_exposure_score=max_exposure,
            projected_risk_score=max_risk,
            campaign_association=primary_campaign,
            created_at=now.isoformat(),
        )

        self._events[tenant_id][event_id] = event
        return event

    def list_correlated_events(self, tenant_id: str = "default_tenant") -> List[CorrelatedExposureEventDTO]:
        """Lists all correlated exposure events for a tenant."""
        return list(self._events.get(tenant_id, {}).values())
