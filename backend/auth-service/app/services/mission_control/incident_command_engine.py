"""
TruthShield X — Incident Command Engine

Manages the incident command lifecycle with strict state-machine transitions,
severity/confidence separation, and evidence-based declaration levels.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    IncidentCommandDTO,
    CommandStatusLiteral,
    CommandSeverityLiteral,
    DeclarationLevelLiteral,
    VALID_COMMAND_TRANSITIONS,
    IncidentEvidenceItemDTO,
    EvidenceConflictDTO,
    IncidentEvidenceRoomDTO,
    IncidentDecisionLogDTO,
    IncidentEscalationDTO,
)


class InvalidTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
    pass


class IncidentNotConfirmedError(Exception):
    """Raised when attempting to close/resolve without verification."""
    pass


class IncidentCommandEngine:
    """Incident Command lifecycle manager with state machine and evidence room."""

    def __init__(self):
        self._commands: Dict[str, IncidentCommandDTO] = {}
        self._evidence_rooms: Dict[str, IncidentEvidenceRoomDTO] = {}
        self._decision_logs: Dict[str, List[IncidentDecisionLogDTO]] = {}
        self._escalations: Dict[str, List[IncidentEscalationDTO]] = {}

    def create_incident_command(
        self,
        tenant_id: str,
        incident_id: str,
        severity: CommandSeverityLiteral,
        confidence: float,
        evidence_strength: float,
        incident_commander: str,
        triggering_signals: Optional[List[str]] = None,
    ) -> IncidentCommandDTO:
        """Creates a new incident command in DETECTED state."""
        cmd = IncidentCommandDTO(
            tenant_id=tenant_id,
            incident_id=incident_id,
            severity=severity,
            confidence=confidence,
            evidence_strength=evidence_strength,
            command_status="DETECTED",
            declaration_level="OBSERVATION",
            incident_commander=incident_commander,
            triggering_signals=triggering_signals or [],
        )
        self._commands[cmd.incident_command_id] = cmd
        self._evidence_rooms[cmd.incident_command_id] = IncidentEvidenceRoomDTO(
            incident_command_id=cmd.incident_command_id
        )
        self._decision_logs[cmd.incident_command_id] = []
        self._escalations[cmd.incident_command_id] = []
        return cmd

    def get_command(self, command_id: str, tenant_id: str = "default_tenant") -> Optional[IncidentCommandDTO]:
        """Retrieves an incident command with tenant isolation."""
        cmd = self._commands.get(command_id)
        if cmd and cmd.tenant_id != tenant_id:
            return None  # Tenant isolation
        return cmd

    def list_commands(self, tenant_id: str = "default_tenant") -> List[IncidentCommandDTO]:
        """Lists incident commands for a tenant."""
        return [c for c in self._commands.values() if c.tenant_id == tenant_id]

    def transition_state(
        self,
        command_id: str,
        new_status: CommandStatusLiteral,
        actor: str = "SYSTEM",
        reason: str = "",
        tenant_id: str = "default_tenant",
    ) -> IncidentCommandDTO:
        """Transitions incident command state with validation."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            raise ValueError(f"Incident command {command_id} not found.")

        current = cmd.command_status
        allowed = VALID_COMMAND_TRANSITIONS.get(current, [])
        if new_status not in allowed:
            raise InvalidTransitionError(
                f"Invalid transition: {current} → {new_status}. Allowed: {allowed}"
            )

        # Block resolution without verification evidence
        if new_status == "RESOLVED":
            room = self._evidence_rooms.get(command_id)
            if room and room.total_verified == 0:
                raise IncidentNotConfirmedError(
                    "Cannot resolve incident without verified evidence."
                )

        cmd.command_status = new_status
        cmd.updated_at = datetime.now(timezone.utc).isoformat()

        if new_status == "RESOLVED":
            cmd.resolved_at = cmd.updated_at

        # Record decision log entry
        self._decision_logs[command_id].append(
            IncidentDecisionLogDTO(
                incident_command_id=command_id,
                decision=f"State transition: {current} → {new_status}",
                reasoning=reason,
                decision_maker=actor,
            )
        )

        return cmd

    def declare_incident_level(
        self,
        command_id: str,
        level: DeclarationLevelLiteral,
        reason: str,
        evidence_references: List[str],
        confidence: float,
        actor: str,
        tenant_id: str = "default_tenant",
    ) -> IncidentCommandDTO:
        """Formally declares incident severity level."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            raise ValueError(f"Incident command {command_id} not found.")

        cmd.declaration_level = level
        cmd.confidence = confidence
        cmd.declared_at = datetime.now(timezone.utc).isoformat()
        cmd.updated_at = cmd.declared_at

        self._decision_logs[command_id].append(
            IncidentDecisionLogDTO(
                incident_command_id=command_id,
                decision=f"Declaration: {level}",
                reasoning=reason,
                evidence_references=evidence_references,
                decision_maker=actor,
            )
        )

        return cmd

    def add_evidence(
        self,
        command_id: str,
        source: str,
        classification: str,
        confidence: float,
        description: str,
        payload: Optional[Dict[str, Any]] = None,
        tenant_id: str = "default_tenant",
    ) -> IncidentEvidenceItemDTO:
        """Adds classified evidence to the incident evidence room."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            raise ValueError(f"Incident command {command_id} not found.")

        item = IncidentEvidenceItemDTO(
            incident_command_id=command_id,
            source=source,
            classification=classification,
            confidence=confidence,
            description=description,
            payload=payload or {},
        )

        room = self._evidence_rooms[command_id]
        room.evidence_items.append(item)

        # Update counters
        if classification == "VERIFIED":
            room.total_verified += 1
        elif classification == "CONFLICTING":
            room.total_conflicting += 1
        else:
            room.total_unverified += 1

        return item

    def register_evidence_conflict(
        self,
        command_id: str,
        evidence_a_id: str,
        evidence_b_id: str,
        conflict_description: str,
        source_a_reliability: float = 0.5,
        source_b_reliability: float = 0.5,
        tenant_id: str = "default_tenant",
    ) -> EvidenceConflictDTO:
        """Registers a conflict between two evidence items."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            raise ValueError(f"Incident command {command_id} not found.")

        conflict = EvidenceConflictDTO(
            incident_command_id=command_id,
            evidence_a_id=evidence_a_id,
            evidence_b_id=evidence_b_id,
            source_a_reliability=source_a_reliability,
            source_b_reliability=source_b_reliability,
            conflict_description=conflict_description,
        )

        self._evidence_rooms[command_id].conflicts.append(conflict)
        self._evidence_rooms[command_id].total_conflicting += 1
        return conflict

    def get_evidence_room(self, command_id: str, tenant_id: str = "default_tenant") -> Optional[IncidentEvidenceRoomDTO]:
        """Returns the evidence room with tenant isolation."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            return None
        return self._evidence_rooms.get(command_id)

    def get_decision_log(self, command_id: str, tenant_id: str = "default_tenant") -> List[IncidentDecisionLogDTO]:
        """Returns the decision log with tenant isolation."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            return []
        return self._decision_logs.get(command_id, [])

    def escalate(
        self,
        command_id: str,
        trigger: str,
        from_level: str,
        to_level: str,
        escalated_by: str = "SYSTEM",
        tenant_id: str = "default_tenant",
    ) -> IncidentEscalationDTO:
        """Escalates an incident."""
        cmd = self.get_command(command_id, tenant_id)
        if not cmd:
            raise ValueError(f"Incident command {command_id} not found.")

        esc = IncidentEscalationDTO(
            incident_command_id=command_id,
            trigger=trigger,
            from_level=from_level,
            to_level=to_level,
            escalated_by=escalated_by,
        )

        self._escalations[command_id].append(esc)
        return esc
