"""
TruthShield X — State Conflict Resolution Engine (Phase 29).

Identifies and preserves contradictory subsystem states as STATE_CONFLICT rather than silently picking arbitrary values.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.mission_control_os_models import StateConflictDTO


class StateConflictResolutionEngine:
    """Detects and registers conflicts across subsystem reports to guarantee epistemic integrity."""

    def __init__(self):
        self._conflicts: Dict[str, StateConflictDTO] = {}

    def register_state_conflict(
        self,
        entity_type: str,
        entity_id: str,
        subsystem_a: str,
        state_a: str,
        subsystem_b: str,
        state_b: str,
    ) -> StateConflictDTO:
        dto = StateConflictDTO(
            entity_type=entity_type,
            entity_id=entity_id,
            subsystem_a=subsystem_a,
            state_a=state_a,
            subsystem_b=subsystem_b,
            state_b=state_b,
            status="STATE_CONFLICT",
            detected_at=datetime.now(timezone.utc).isoformat(),
        )
        self._conflicts[dto.conflict_id] = dto
        return dto

    def list_conflicts(self) -> List[StateConflictDTO]:
        return list(self._conflicts.values())
