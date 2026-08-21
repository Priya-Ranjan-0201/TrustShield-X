"""Idempotent Intelligence Event Bus with Dead-Letter Handling (Phase 4.0 Part 6 — Sections 19-22, 85-87).

Provides at-least-once processing guarantees, idempotent delivery via deduplication keys,
and dead-letter queue (DLQ) support for unrecoverable errors.
"""

from typing import List, Dict, Any, Optional, Callable, Awaitable
import hashlib
import uuid
from datetime import datetime, timezone
from app.schemas.continuous_intelligence_models import (
    IntelligenceEventDTO,
    EventProcessingRecordDTO,
    EventDeadLetterDTO,
)


class DuplicateEventError(Exception):
    """Raised when an identical event has already been published/processed."""
    pass


class IntelligenceEventBus:
    """In-memory asynchronous event bus with idempotent routing and DLQ support."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[IntelligenceEventDTO], Any]]] = {}
        self._published_events: Dict[str, IntelligenceEventDTO] = {}
        self._dedup_keys: Dict[str, str] = {}  # dedup_key -> event_id
        self._processing_records: Dict[str, EventProcessingRecordDTO] = {}
        self._dead_letters: Dict[str, EventDeadLetterDTO] = {}
        self._sequence: int = 0

    def compute_deduplication_key(self, event: IntelligenceEventDTO) -> str:
        """Generate deterministic deduplication key (Section 22)."""
        raw = f"{event.event_type}:{event.entity_id or ''}:{event.analysis_id or ''}:{event.event_version}:{event.payload.get('indicator_value_hash', '')}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def subscribe(self, event_type: str, handler: Callable[[IntelligenceEventDTO], Any]) -> None:
        """Register consumer handler for an event type or wildcard '*'."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: IntelligenceEventDTO) -> bool:
        """Publish event with idempotency check. Returns True if accepted, False if duplicate."""
        if not event.deduplication_key:
            event.deduplication_key = self.compute_deduplication_key(event)

        if event.deduplication_key in self._dedup_keys:
            # Duplicate event detected -> ignore safely without duplicating alerts/actions (Test 7)
            return False

        self._published_events[event.event_id] = event
        self._dedup_keys[event.deduplication_key] = event.event_id
        self._sequence += 1

        # Dispatch to subscribed handlers
        handlers = self._handlers.get(event.event_type, []) + self._handlers.get("*", [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as ex:
                self.dead_letter(event, str(ex), consumer=getattr(handler, "__name__", "anonymous_consumer"))

        return True

    def acknowledge(self, event_id: str, consumer_id: str) -> EventProcessingRecordDTO:
        """Mark event as processed by consumer."""
        record = EventProcessingRecordDTO(
            record_id=f"epr_{uuid.uuid4().hex[:12]}",
            event_id=event_id,
            consumer_id=consumer_id,
            status="PROCESSED",
            processed_at=datetime.now(timezone.utc).isoformat(),
        )
        self._processing_records[f"{event_id}:{consumer_id}"] = record
        return record

    def dead_letter(self, event: IntelligenceEventDTO, error: str, consumer: str) -> EventDeadLetterDTO:
        """Route failed event to dead-letter queue (Sections 86-87)."""
        self._published_events[event.event_id] = event
        dl = EventDeadLetterDTO(
            dead_letter_id=f"edl_{uuid.uuid4().hex[:12]}",
            event_id=event.event_id,
            error=error,
            attempts=1,
            last_attempt=datetime.now(timezone.utc).isoformat(),
            consumer=consumer,
            payload_reference=f"event:{event.event_id}",
            status="PENDING",
        )
        self._dead_letters[dl.dead_letter_id] = dl
        return dl


    def reprocess_dead_letter(self, dead_letter_id: str, reprocessed_by: str = "ADMIN") -> Optional[IntelligenceEventDTO]:
        """Reprocess a dead-letter event with audit tracking (Section 87)."""
        dl = self._dead_letters.get(dead_letter_id)
        if not dl or dl.status == "RESOLVED":
            return None

        event = self._published_events.get(dl.event_id)
        if not event:
            return None

        dl.status = "RESOLVED"
        dl.reprocessed_at = datetime.now(timezone.utc).isoformat()
        dl.reprocessed_by = reprocessed_by

        # Re-dispatch event
        handlers = self._handlers.get(event.event_type, []) + self._handlers.get("*", [])
        for handler in handlers:
            handler(event)

        return event

    def get_events(self, since_sequence: int = 0) -> List[IntelligenceEventDTO]:
        """Fetch all events published."""
        return list(self._published_events.values())

    def get_dead_letters(self) -> List[EventDeadLetterDTO]:
        """Fetch all dead letters."""
        return list(self._dead_letters.values())
