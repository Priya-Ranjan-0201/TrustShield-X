"""
TruthShield X — Incident Command Engine (Phase 21).

Manages RBAC-controlled Incident Command assignments.
"""

from typing import Dict, Optional
from datetime import datetime, timezone
from app.schemas.autonomous_soc_models import IncidentCommandStructureDTO


class IncidentCommandEngine:
    """Assigns and coordinates Incident Command roles (Commander, Technical Lead, Comms, Recovery)."""

    def __init__(self):
        self._commands: Dict[str, IncidentCommandStructureDTO] = {}

    def assign_command_team(
        self,
        incident_id: str,
        commander: str,
        technical_lead: str,
        comms_lead: str,
        recovery_lead: str,
        security_analyst: str,
    ) -> IncidentCommandStructureDTO:
        structure = IncidentCommandStructureDTO(
            incident_id=incident_id,
            incident_commander=commander,
            technical_lead=technical_lead,
            comms_lead=comms_lead,
            recovery_lead=recovery_lead,
            security_analyst=security_analyst,
            assigned_at=datetime.now(timezone.utc).isoformat(),
        )
        self._commands[incident_id] = structure
        return structure

    def get_command_team(self, incident_id: str) -> Optional[IncidentCommandStructureDTO]:
        return self._commands.get(incident_id)
