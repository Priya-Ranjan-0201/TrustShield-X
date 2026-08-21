"""
TruthShield X — Collective Threat Detection Engine (Phase 28).

Identifies coordinated threat campaigns emerging across multiple authorized organizations.
"""

from typing import Dict, List, Any
from datetime import datetime, timezone


class CollectiveThreatDetectionEngine:
    """Detects multi-tenant campaign emergence and coordinated targeting patterns across participating peers."""

    def detect_collective_campaigns(
        self,
        tenant_events: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        # Count campaign hits across unique tenants
        campaign_tenants: Dict[str, set] = {}
        for event in tenant_events:
            cmp_id = event.get("campaign_id", "cmp_unknown")
            t_id = event.get("tenant_id", "default_tenant")
            if cmp_id not in campaign_tenants:
                campaign_tenants[cmp_id] = set()
            campaign_tenants[cmp_id].add(t_id)

        collective_campaigns = []
        for cmp_id, tenants in campaign_tenants.items():
            if len(tenants) >= 2:
                collective_campaigns.append({
                    "campaign_id": cmp_id,
                    "affected_tenant_count": len(tenants),
                    "participating_tenants": list(tenants),
                    "detection_level": "COLLECTIVE_CAMPAIGN_SURGE",
                    "requires_coordination": True,
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                })

        return collective_campaigns
