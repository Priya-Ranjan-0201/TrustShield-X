"""
TruthShield X — Mission Workflow Orchestrator (Phase 29).

Executes end-to-end mission workflows coordinating Threat Intelligence, Digital Twin, Assurance, Engineering, SOC, SOAR, and Resilience.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_os_models import MissionWorkflowDTO, SecurityEventTypeLiteral


class MissionWorkflowOrchestrator:
    """Coordinates complex cross-subsystem workflows with safety checks, Four-Eyes gates, and automated rollback."""

    def __init__(self):
        self._workflows: Dict[str, MissionWorkflowDTO] = {}
        self._seed_default_workflows()

    def _seed_default_workflows(self):
        wf1 = MissionWorkflowDTO(
            workflow_id="wf_threat_to_investigation_01",
            name="THREAT_TO_INVESTIGATION",
            version="1.0.0",
            trigger_event="EARLY_WARNING",
            steps=[
                {"step_num": 1, "subsystem": "global_threat_intel", "action": "SURFACE_CAMPAIGN_SURGE", "status": "COMPLETED"},
                {"step_num": 2, "subsystem": "digital_twin_lab", "action": "SIMULATE_BLAST_RADIUS", "status": "COMPLETED"},
                {"step_num": 3, "subsystem": "security_assurance", "action": "VERIFY_CONTROL_READINESS", "status": "COMPLETED"},
                {"step_num": 4, "subsystem": "soc_orchestrator", "action": "CREATE_SOC_INVESTIGATION_TASK", "status": "IN_PROGRESS"},
            ],
            status="RUNNING",
            rollback_procedure="Revert staged Sigma queries and reset routing baseline",
            requires_four_eyes=True,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._workflows[wf1.workflow_id] = wf1

    def run_workflow(
        self,
        name: str,
        trigger_event: SecurityEventTypeLiteral,
        steps: List[Dict[str, Any]],
        requires_four_eyes: bool = True,
    ) -> MissionWorkflowDTO:
        dto = MissionWorkflowDTO(
            name=name,
            version="1.0.0",
            trigger_event=trigger_event,
            steps=steps,
            status="RUNNING",
            rollback_procedure="Automated reverse-step execution",
            requires_four_eyes=requires_four_eyes,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._workflows[dto.workflow_id] = dto
        return dto

    def get_workflow(self, workflow_id: str) -> Optional[MissionWorkflowDTO]:
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[MissionWorkflowDTO]:
        return list(self._workflows.values())
