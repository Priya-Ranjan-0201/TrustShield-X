"""Unit Tests — Real-Time Event Hub, Subscriptions & Scopes (Phase 4.0 Part 6 — Sections 51-56, 107).

Implements:
- Mandatory Test 15: Client reconnects -> missed-event recovery.
- Mandatory Test 16: User lacks access to case -> no real-time events from that case.
- Mandatory Test 17: Organization A subscribes -> Organization B events are strictly invisible.
"""

from datetime import datetime, timezone, timedelta
import pytest
from app.schemas.continuous_intelligence_models import IntelligenceEventDTO
from app.services.monitoring.realtime_hub import RealtimeHub


class TestRealtimeAuthAndRecovery:
    def test_15_mandatory_reconnect_and_missed_event_recovery(self):
        hub = RealtimeHub()
        hub.subscribe(client_id="client_101", user_id="user_1", organization_id="org_a")

        past_time = (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat()
        current_time = datetime.now(timezone.utc).isoformat()

        evt = IntelligenceEventDTO(
            event_id="evt_rec_1",
            event_type="IOC_NEW",
            timestamp=current_time,
            correlation_id="corr_rec",
            payload={"organization_id": "org_a"},
        )
        hub.dispatch_event(evt)

        # Recover events missed since past_time
        recovered = hub.recover_missed_events("client_101", since_timestamp=past_time)
        assert len(recovered) == 1
        assert recovered[0].event_id == "evt_rec_1"

    def test_16_mandatory_case_isolation(self):
        hub = RealtimeHub()
        # Client only authorized for Case A
        hub.subscribe(client_id="client_case_a", user_id="user_a", case_ids=["case_A"])

        evt_case_b = IntelligenceEventDTO(
            event_id="evt_case_b",
            event_type="THREAT_MATCH_NEW",
            case_id="case_B",
            correlation_id="corr_b",
        )
        notified = hub.dispatch_event(evt_case_b)
        assert "client_case_a" not in notified

    def test_17_mandatory_multi_tenant_isolation(self):
        hub = RealtimeHub()
        hub.subscribe(client_id="client_org_a", user_id="user_a", organization_id="org_alpha")

        evt_org_b = IntelligenceEventDTO(
            event_id="evt_org_b",
            event_type="THREAT_MATCH_NEW",
            correlation_id="corr_b",
            payload={"organization_id": "org_beta"},
        )
        notified = hub.dispatch_event(evt_org_b)
        assert "client_org_a" not in notified
