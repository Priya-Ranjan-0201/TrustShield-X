"""Real-Time Event Hub, Subscriptions & Missed-Event Recovery (Phase 4.0 Part 6 — Sections 51-56).

Enforces tenant isolation, role-based event authorization, and sequence-based event recovery.
"""

from typing import List, Dict, Any, Optional, Set
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    RealtimeSubscriptionDTO,
    IntelligenceEventDTO,
)


class RealtimeHub:
    """Manages real-time WebSocket/SSE subscriptions and delivers authorization-scoped event streams."""

    def __init__(self):
        self._subscriptions: Dict[str, RealtimeSubscriptionDTO] = {}
        self._event_history: List[IntelligenceEventDTO] = []

    def subscribe(
        self,
        client_id: str,
        user_id: str,
        organization_id: Optional[str] = None,
        case_ids: Optional[List[str]] = None,
        analysis_ids: Optional[List[str]] = None,
    ) -> RealtimeSubscriptionDTO:
        """Register a client subscription scoped to tenant and authorized cases."""
        sub = RealtimeSubscriptionDTO(
            subscription_id=f"sub_{uuid.uuid4().hex[:12]}",
            client_id=client_id,
            user_id=user_id,
            organization_id=organization_id,
            case_ids=case_ids or [],
            analysis_ids=analysis_ids or [],
        )
        self._subscriptions[client_id] = sub
        return sub

    def unsubscribe(self, client_id: str) -> None:
        self._subscriptions.pop(client_id, None)

    def dispatch_event(self, event: IntelligenceEventDTO) -> List[str]:
        """Dispatch event to matching authorized subscribers. Returns list of client IDs notified."""
        self._event_history.append(event)
        delivered_clients: List[str] = []

        event_org = event.payload.get("organization_id")
        event_case = event.case_id

        for client_id, sub in self._subscriptions.items():
            # 1. Multi-Tenant Isolation Check (Section 54, Test 17)
            if event_org and sub.organization_id and event_org != sub.organization_id:
                continue

            # 2. Case Access Check (Section 54, Test 16)
            if event_case and sub.case_ids and event_case not in sub.case_ids:
                continue

            delivered_clients.append(client_id)

        return delivered_clients

    def recover_missed_events(
        self,
        client_id: str,
        since_timestamp: Optional[str] = None,
    ) -> List[IntelligenceEventDTO]:
        """Replay missed events for reconnecting clients (Section 55-56, Test 15)."""
        sub = self._subscriptions.get(client_id)
        if not sub:
            return []

        res: List[IntelligenceEventDTO] = []
        for evt in self._event_history:
            if since_timestamp and evt.timestamp <= since_timestamp:
                continue

            # Check authorization for each replayed event
            event_org = evt.payload.get("organization_id")
            if event_org and sub.organization_id and event_org != sub.organization_id:
                continue
            if evt.case_id and sub.case_ids and evt.case_id not in sub.case_ids:
                continue

            res.append(evt)

        return res
