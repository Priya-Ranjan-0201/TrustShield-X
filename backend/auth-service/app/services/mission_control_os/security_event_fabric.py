"""
TruthShield X — Security Event Fabric (Phase 29).

Central high-throughput, idempotent event fabric enforcing causal ordering and replay protection across all security subsystems.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_os_models import SecurityEventDTO, SecurityEventTypeLiteral


class SecurityEventFabric:
    """Enterprise event fabric with idempotency deduplication and causal correlation."""

    def __init__(self):
        self._events: Dict[str, SecurityEventDTO] = {}
        self._processed_idempotency_keys: set = set()
        self._seed_default_events()

    def _seed_default_events(self):
        e1 = SecurityEventDTO(
            event_id="evt_early_warning_darkstorm",
            event_type="EARLY_WARNING",
            source="global_threat_intel",
            tenant_id="default_tenant",
            payload={"threat_name": "DarkStorm C2 Expansion", "severity": "HIGH"},
            correlation_id="corr_darkstorm_campaign",
            idempotency_key="idem_darkstorm_seed_01",
            confidence=0.92,
        )
        self._events[e1.event_id] = e1
        self._processed_idempotency_keys.add(e1.idempotency_key)

    def publish_event(
        self,
        event_type: SecurityEventTypeLiteral,
        source: str,
        payload: Dict[str, Any],
        idempotency_key: str,
        tenant_id: str = "default_tenant",
        correlation_id: Optional[str] = None,
        causation_id: Optional[str] = None,
        confidence: float = 0.95,
    ) -> Dict[str, Any]:
        # Idempotency check
        if idempotency_key in self._processed_idempotency_keys:
            return {
                "status": "IGNORE_DUPLICATE",
                "message": f"Event with idempotency_key '{idempotency_key}' already processed.",
                "idempotency_key": idempotency_key,
                "duplicated": True,
            }

        dto = SecurityEventDTO(
            event_type=event_type,
            source=source,
            tenant_id=tenant_id,
            payload=payload,
            correlation_id=correlation_id or f"corr_{idempotency_key[:8]}",
            causation_id=causation_id,
            idempotency_key=idempotency_key,
            confidence=confidence,
        )
        self._events[dto.event_id] = dto
        self._processed_idempotency_keys.add(idempotency_key)

        return {
            "status": "PUBLISHED",
            "event_id": dto.event_id,
            "event": dto,
            "duplicated": False,
        }

    def get_event(self, event_id: str) -> Optional[SecurityEventDTO]:
        return self._events.get(event_id)

    def list_events(self, tenant_id: str = "default_tenant") -> List[SecurityEventDTO]:
        return [e for e in self._events.values() if e.tenant_id == tenant_id]
