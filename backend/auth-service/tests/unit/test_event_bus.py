"""Unit Tests — Intelligence Event Bus, Idempotency & DLQ (Phase 4.0 Part 6 — Sections 19-22, 85-87, 107).

Implements:
- Mandatory Test 7: Same event delivered twice -> exactly one effective processing.
- Mandatory Test 8: Event fails repeatedly -> routed to dead-letter queue.
- Mandatory Test 9: Dead-letter event reprocessed -> audited reprocessing.
"""

import pytest
from app.schemas.continuous_intelligence_models import IntelligenceEventDTO
from app.services.monitoring.intelligence_event_bus import IntelligenceEventBus


class TestIntelligenceEventBus:
    def test_07_mandatory_same_event_delivered_twice_is_idempotent(self):
        bus = IntelligenceEventBus()
        processed_count = [0]

        def _handler(evt: IntelligenceEventDTO):
            processed_count[0] += 1

        bus.subscribe("IOC_NEW", _handler)

        event = IntelligenceEventDTO(
            event_id="evt_100",
            event_type="IOC_NEW",
            entity_id="domain_123",
            correlation_id="corr_1",
            payload={"indicator_value_hash": "hash_123"},
        )

        res1 = bus.publish(event)
        res2 = bus.publish(event)

        assert res1 is True
        assert res2 is False  # Deduplicated
        assert processed_count[0] == 1

    def test_08_mandatory_failing_event_routed_to_dead_letter_queue(self):
        bus = IntelligenceEventBus()

        def _faulty_handler(evt: IntelligenceEventDTO):
            raise RuntimeError("Database connection timed out")

        bus.subscribe("IOC_NEW", _faulty_handler)

        event = IntelligenceEventDTO(
            event_id="evt_fail_1",
            event_type="IOC_NEW",
            entity_id="hash_fail",
            correlation_id="corr_2",
            payload={"indicator_value_hash": "hash_fail"},
        )

        bus.publish(event)
        dlqs = bus.get_dead_letters()
        assert len(dlqs) == 1
        assert dlqs[0].event_id == "evt_fail_1"
        assert "Database connection timed out" in dlqs[0].error

    def test_09_mandatory_dead_letter_reprocessing_audited(self):
        bus = IntelligenceEventBus()
        success_flag = [False]

        # Handler that succeeds on second try
        def _reprocess_handler(evt: IntelligenceEventDTO):
            success_flag[0] = True

        bus.subscribe("IOC_NEW", _reprocess_handler)

        event = IntelligenceEventDTO(
            event_id="evt_dlq_reprocess",
            event_type="IOC_NEW",
            entity_id="entity_reprocess",
            correlation_id="corr_3",
            payload={"indicator_value_hash": "h_rep"},
        )
        dl = bus.dead_letter(event, "Temporary network blip", consumer="test_consumer")

        # Reprocess
        reprocessed = bus.reprocess_dead_letter(dl.dead_letter_id, reprocessed_by="SOC_LEAD_ADMIN")
        assert reprocessed is not None
        assert dl.status == "RESOLVED"
        assert dl.reprocessed_by == "SOC_LEAD_ADMIN"
        assert success_flag[0] is True
