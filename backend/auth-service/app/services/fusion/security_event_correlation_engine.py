"""
TruthShield X — Security Event Correlation Engine
"""

import uuid
from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.fusion_models import SecurityEventDTO, EventCorrelationResultDTO


class SecurityEventCorrelationEngine:
    """Correlates security events across entities, assets, campaigns, infrastructure, and indicators."""

    def __init__(self):
        # tenant_id -> correlation_id -> EventCorrelationResultDTO
        self._correlations: Dict[str, Dict[str, EventCorrelationResultDTO]] = {}

    def correlate_events(
        self,
        events: List[SecurityEventDTO],
        correlation_type: str = "MULTI_MODAL_INDICATOR_CONVERGENCE",
        tenant_id: str = "default_tenant",
    ) -> Optional[EventCorrelationResultDTO]:
        """Correlates a collection of events based on shared indicators and campaigns."""
        if len(events) < 2:
            return None

        # Check common linkage
        common_entities = set(e.entity_id for e in events if e.entity_id)
        common_campaigns = set(e.campaign_id for e in events if e.campaign_id)
        common_assets = set(e.asset_id for e in events if e.asset_id)

        # Baseline confidence calculation
        avg_confidence = sum(e.confidence for e in events) / len(events)
        boost = 0.10 if (common_campaigns or common_entities or common_assets) else 0.0
        final_conf = max(0.0, min(1.0, avg_confidence + boost))

        correlation_id = f"corr_{uuid.uuid4().hex[:12]}"
        supporting_ids = [e.event_id for e in events]

        reason = (
            f"Correlated {len(events)} events across {len(common_entities)} entities, "
            f"{len(common_assets)} assets, and {len(common_campaigns)} campaigns."
        )

        result = EventCorrelationResultDTO(
            correlation_id=correlation_id,
            correlation_type=correlation_type,
            confidence=round(final_conf, 3),
            supporting_event_ids=supporting_ids,
            counter_event_ids=[],
            reason=reason,
            tenant_id=tenant_id,
            correlated_at=datetime.now(timezone.utc).isoformat(),
        )

        if tenant_id not in self._correlations:
            self._correlations[tenant_id] = {}
        self._correlations[tenant_id][correlation_id] = result

        # Annotate events with correlation_id
        for e in events:
            e.correlation_id = correlation_id

        return result

    def get_correlation(self, correlation_id: str, tenant_id: str = "default_tenant") -> Optional[EventCorrelationResultDTO]:
        """Retrieves a correlation result."""
        return self._correlations.get(tenant_id, {}).get(correlation_id)

    def list_correlations(self, tenant_id: str = "default_tenant") -> List[EventCorrelationResultDTO]:
        """Lists all correlations for a tenant."""
        return list(self._correlations.get(tenant_id, {}).values())
