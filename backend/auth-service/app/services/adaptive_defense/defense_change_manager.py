"""
TruthShield X — Defense Change Manager & Collision Engine (Phase 17).

Coordinates change scheduling, collision detection, and operator overrides.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
import uuid

from app.schemas.adaptive_defense_models import DefenseChangeRecordDTO


class DefenseChangeManager:
    """Manages defense change lifecycle, collision prevention, and manual overrides."""

    def __init__(self):
        # change_id -> DefenseChangeRecordDTO
        self._changes: Dict[str, DefenseChangeRecordDTO] = {}
        self._active_target_locks: Dict[str, str] = {}  # target -> change_id

    def schedule_change(
        self,
        tenant_id: str,
        action_type: str,
        target: str,
        reason: str,
        evidence_references: Optional[List[str]] = None,
        executor: str = "SOC_AUTOMATION",
        is_time_bounded: bool = False,
        expires_at: Optional[str] = None,
    ) -> DefenseChangeRecordDTO:
        """Schedules a new defense adaptation change."""
        # Collision Detection (Section 53)
        if target in self._active_target_locks:
            existing_id = self._active_target_locks[target]
            raise ValueError(f"Change collision detected: Target '{target}' is currently locked by change '{existing_id}'.")

        change = DefenseChangeRecordDTO(
            tenant_id=tenant_id,
            action_type=action_type,
            target=target,
            reason=reason,
            evidence_references=evidence_references or [],
            executor=executor,
            is_time_bounded=is_time_bounded,
            expires_at=expires_at,
        )

        self._changes[change.change_id] = change
        self._active_target_locks[target] = change.change_id
        return change

    def record_execution_result(
        self,
        change_id: str,
        status: str,
        rollback_state: Optional[Dict[str, Any]] = None,
    ) -> Optional[DefenseChangeRecordDTO]:
        """Updates execution status and releases target lock if completed."""
        change = self._changes.get(change_id)
        if not change:
            return None

        change.execution_status = status  # type: ignore
        change.executed_at = datetime.now(timezone.utc).isoformat()
        if rollback_state:
            change.rollback_state = rollback_state

        if status in ("SUCCEEDED", "FAILED", "ROLLED_BACK") and change.target in self._active_target_locks:
            del self._active_target_locks[change.target]

        return change

    def get_change(self, change_id: str) -> Optional[DefenseChangeRecordDTO]:
        return self._changes.get(change_id)

    def list_changes(self, tenant_id: str = "default_tenant") -> List[DefenseChangeRecordDTO]:
        return [c for c in self._changes.values() if c.tenant_id == tenant_id]
