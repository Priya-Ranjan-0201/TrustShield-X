"""
TruthShield X — Incident State Machine Engine (Phase 21).

Enforces strict lifecycle state transitions and rejects illegal mutations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import IncidentStateMachineDTO, SOCIncidentStateLiteral


class IncidentStateMachine:
    """Enforces strict deterministic state transitions for SOC incidents."""

    ALLOWED_TRANSITIONS: Dict[SOCIncidentStateLiteral, List[SOCIncidentStateLiteral]] = {
        "NEW": ["TRIAGED", "CANCELLED"],
        "TRIAGED": ["INVESTIGATING", "ESCALATED", "CANCELLED"],
        "INVESTIGATING": ["CONTAINMENT_PENDING", "ESCALATED", "CANCELLED"],
        "CONTAINMENT_PENDING": ["CONTAINED", "ESCALATED"],
        "CONTAINED": ["ERADICATION", "ESCALATED"],
        "ERADICATION": ["RECOVERY", "ESCALATED"],
        "RECOVERY": ["VALIDATION", "ESCALATED"],
        "VALIDATION": ["CLOSED", "REOPENED"],
        "CLOSED": ["REOPENED"],
        "REOPENED": ["INVESTIGATING", "TRIAGED"],
        "ESCALATED": ["INVESTIGATING", "CONTAINMENT_PENDING", "CONTAINED"],
        "CANCELLED": ["REOPENED"],
    }

    def __init__(self):
        self._machines: Dict[str, IncidentStateMachineDTO] = {}

    def init_incident(self, incident_id: str) -> IncidentStateMachineDTO:
        dto = IncidentStateMachineDTO(
            incident_id=incident_id,
            current_state="NEW",
            state_history=[{"state": "NEW", "timestamp": datetime.now(timezone.utc).isoformat(), "actor": "SYSTEM"}],
            allowed_next_states=self.ALLOWED_TRANSITIONS["NEW"],
        )
        self._machines[incident_id] = dto
        return dto

    def transition(self, incident_id: str, new_state: SOCIncidentStateLiteral, actor: str = "usr_analyst_01") -> IncidentStateMachineDTO:
        machine = self._machines.get(incident_id)
        if not machine:
            machine = self.init_incident(incident_id)

        if new_state not in self.ALLOWED_TRANSITIONS.get(machine.current_state, []):
            raise ValueError(f"Illegal state transition from '{machine.current_state}' to '{new_state}'.")

        updated_history = list(machine.state_history) + [
            {"state": new_state, "timestamp": datetime.now(timezone.utc).isoformat(), "actor": actor}
        ]

        updated = IncidentStateMachineDTO(
            incident_id=incident_id,
            current_state=new_state,
            state_history=updated_history,
            allowed_next_states=self.ALLOWED_TRANSITIONS.get(new_state, []),
            updated_at=datetime.now(timezone.utc).isoformat(),
        )
        self._machines[incident_id] = updated
        return updated

    def get_machine(self, incident_id: str) -> Optional[IncidentStateMachineDTO]:
        return self._machines.get(incident_id)
