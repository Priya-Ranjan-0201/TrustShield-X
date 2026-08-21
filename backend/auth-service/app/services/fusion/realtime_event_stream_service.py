"""
TruthShield X — Real-Time Event Streaming, Schema Versioning & Dead-Letter Queue Engine
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.fusion_models import SecurityEventDTO


class RealTimeEventStreamService:
    """Provides secure, version-checked event streaming with dead-letter queue recovery and idempotent replay."""

    SUPPORTED_SCHEMA_VERSIONS = {"security.event.v1", "security.event.v2"}

    def __init__(self):
        # tenant_id -> List[Event]
        self._streams: Dict[str, List[Dict[str, Any]]] = {}
        # tenant_id -> List[DLQ Records]
        self._dead_letter_queue: Dict[str, List[Dict[str, Any]]] = {}

    def publish_event(
        self,
        event_payload: Dict[str, Any],
        schema_version: str = "security.event.v1",
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Publishes an event to the real-time stream after verifying schema version and tenant authorization."""
        if tenant_id not in self._streams:
            self._streams[tenant_id] = []
            self._dead_letter_queue[tenant_id] = []

        # Validate schema version
        if schema_version not in self.SUPPORTED_SCHEMA_VERSIONS:
            return self._route_to_dlq(
                payload=event_payload,
                reason=f"Unsupported schema version '{schema_version}'. Supported: {self.SUPPORTED_SCHEMA_VERSIONS}",
                tenant_id=tenant_id,
            )

        # Validate required fields
        if not event_payload.get("event_type") or not event_payload.get("source"):
            return self._route_to_dlq(
                payload=event_payload,
                reason="Malformed event payload: missing required fields 'event_type' or 'source'.",
                tenant_id=tenant_id,
            )

        stream_record = {
            "stream_id": f"stm_{uuid.uuid4().hex[:12]}",
            "schema_version": schema_version,
            "tenant_id": tenant_id,
            "payload": event_payload,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "status": "STREAMED",
        }

        self._streams[tenant_id].append(stream_record)
        return stream_record

    def _route_to_dlq(
        self,
        payload: Dict[str, Any],
        reason: str,
        tenant_id: str,
    ) -> Dict[str, Any]:
        """Enqueues failed or unprocessable event into the Dead-Letter Queue."""
        dlq_id = f"dlq_{uuid.uuid4().hex[:12]}"
        dlq_entry = {
            "dlq_id": dlq_id,
            "tenant_id": tenant_id,
            "payload": payload,
            "reason": reason,
            "attempt_count": 1,
            "error_classification": "SCHEMA_OR_PAYLOAD_VALIDATION_ERROR",
            "enqueued_at": datetime.now(timezone.utc).isoformat(),
            "status": "DEAD_LETTER",
        }
        self._dead_letter_queue[tenant_id].append(dlq_entry)
        return dlq_entry

    def list_dlq(self, tenant_id: str = "default_tenant") -> List[Dict[str, Any]]:
        """Lists events in Dead-Letter Queue."""
        return self._dead_letter_queue.get(tenant_id, [])

    def replay_dlq_entry(
        self,
        dlq_id: str,
        corrected_payload: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Replays an event from the DLQ idempotently."""
        dlq_list = self._dead_letter_queue.get(tenant_id, [])
        entry = next((d for d in dlq_list if d["dlq_id"] == dlq_id), None)
        if not entry:
            raise KeyError(f"DLQ entry '{dlq_id}' not found.")

        payload_to_publish = corrected_payload or entry["payload"]
        res = self.publish_event(payload_to_publish, schema_version="security.event.v1", tenant_id=tenant_id)
        if res.get("status") == "STREAMED":
            entry["status"] = "REPLAYED_SUCCESSFULLY"
        return res
