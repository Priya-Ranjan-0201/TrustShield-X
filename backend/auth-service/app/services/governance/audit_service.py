"""Append-Only Audit Service with SHA-256 Hash Chaining (Phase 4.0 Part 8 — Sections 45-49, 98).

Provides tamper-evident immutable audit trails and blocks any deletion or modification attempts.
"""

from typing import List, Dict, Any, Optional
import hashlib
import json
import uuid
from datetime import datetime, timezone
from app.schemas.governance_models import (
    AuditEventDTO,
    AuditIntegrityCheckpointDTO,
)
from app.services.governance.data_classification_engine import DataClassificationEngine


class AuditService:
    """Append-only audit service with cryptographic hash chaining and integrity verification."""

    def __init__(self):
        self._audit_log: List[AuditEventDTO] = []
        self._last_hash: Optional[str] = None

    def record_event(
        self,
        organization_id: str,
        actor_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        result: str = "SUCCESS",
        reason: str = "",
        actor_type: str = "USER",
        session_reference: Optional[str] = None,
        policy_id: Optional[str] = None,
        policy_version: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> AuditEventDTO:
        audit_id = f"aud_{uuid.uuid4().hex[:12]}"
        now_str = datetime.now(timezone.utc).isoformat()

        # Sanitize metadata (Section 30, Mandatory Test 20)
        clean_meta = DataClassificationEngine.sanitize_dictionary(metadata or {})
        clean_reason = DataClassificationEngine.redact_sensitive_data(reason)

        # Compute SHA-256 hash chaining
        raw = f"{audit_id}:{actor_id}:{action}:{resource_id}:{result}:{clean_reason}:{now_str}:{self._last_hash or ''}"
        event_hash = hashlib.sha256(raw.encode()).hexdigest()

        event = AuditEventDTO(
            audit_id=audit_id,
            organization_id=organization_id,
            actor_type=actor_type,
            actor_id=actor_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            result=result,
            reason=clean_reason,
            previous_hash=self._last_hash,
            event_hash=event_hash,
            session_reference=session_reference,
            policy_id=policy_id,
            policy_version=policy_version,
            metadata=clean_meta,
            timestamp=now_str,
        )

        self._audit_log.append(event)
        self._last_hash = event_hash
        return event

    def delete_event_blocked(self, audit_id: str) -> None:
        """Section 48, Mandatory Test 14: Audit records are append-only; deletion is strictly BLOCKED."""
        raise PermissionError("Access denied: Audit records are immutable and cannot be deleted or suppressed.")

    def verify_integrity(self) -> bool:
        """Section 49, Mandatory Test 13: Verifies entire hash chain for tamper detection."""
        expected_prev = None
        for event in self._audit_log:
            raw = f"{event.audit_id}:{event.actor_id}:{event.action}:{event.resource_id}:{event.result}:{event.reason}:{event.timestamp}:{expected_prev or ''}"
            recomputed = hashlib.sha256(raw.encode()).hexdigest()
            if recomputed != event.event_hash or event.previous_hash != expected_prev:
                return False
            expected_prev = event.event_hash
        return True


    def query_audit_events(
        self,
        organization_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        action: Optional[str] = None,
        resource_type: Optional[str] = None,
        result: Optional[str] = None,
        limit: int = 50,
    ) -> List[AuditEventDTO]:
        events = self._audit_log
        if organization_id:
            events = [e for e in events if e.organization_id == organization_id]
        if actor_id:
            events = [e for e in events if e.actor_id == actor_id]
        if action:
            events = [e for e in events if e.action == action]
        if resource_type:
            events = [e for e in events if e.resource_type == resource_type]
        if result:
            events = [e for e in events if e.result == result]
        return events[-limit:]
