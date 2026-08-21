"""
TruthShield X — Global Security Mission Control Engine (Phase 29 Master Coordinator).

Unified Cyber Defense Operating System orchestrating Threat Intelligence, Digital Twin, Assurance,
Engineering, SOC, SOAR, Incident Command, Resilience, and Knowledge into a single operational command plane.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from app.schemas.mission_control_os_models import (
    UnifiedSecurityStateDTO,
    SecurityEventDTO,
    MissionTaskDTO,
    MissionWorkflowDTO,
    SecurityPostureDTO,
    IncidentCommandMissionDTO,
    MissionControlHealthDTO,
    StateConflictDTO,
)
from app.services.mission_control_os.security_event_fabric import SecurityEventFabric
from app.services.mission_control_os.unified_security_state_engine import UnifiedSecurityStateEngine
from app.services.mission_control_os.mission_priority_engine import MissionPriorityEngine
from app.services.mission_control_os.security_situational_awareness_engine import SecuritySituationalAwarenessEngine
from app.services.mission_control_os.security_posture_engine import SecurityPostureEngine
from app.services.mission_control_os.mission_incident_command_engine import MissionIncidentCommandEngine
from app.services.mission_control_os.mission_task_engine import MissionTaskEngine
from app.services.mission_control_os.mission_sla_engine import MissionSLAEngine
from app.services.mission_control_os.mission_blocker_engine import MissionBlockerEngine
from app.services.mission_control_os.mission_workflow_orchestrator import MissionWorkflowOrchestrator
from app.services.mission_control_os.subsystem_integration_bridge import SubsystemIntegrationBridge
from app.services.mission_control_os.copilot_mission_control_bridge import CopilotMissionControlBridge
from app.services.mission_control_os.realtime_state_streamer import RealtimeStateStreamer
from app.services.mission_control_os.mission_control_health_engine import MissionControlHealthEngine
from app.services.mission_control_os.state_conflict_resolution_engine import StateConflictResolutionEngine


class GlobalSecurityMissionControlEngine:
    """Master Cyber Defense Operating System orchestrator for TruthShield X."""

    def __init__(self):
        self.event_fabric = SecurityEventFabric()
        self.state_engine = UnifiedSecurityStateEngine()
        self.priority_engine = MissionPriorityEngine()
        self.situational_engine = SecuritySituationalAwarenessEngine()
        self.posture_engine = SecurityPostureEngine()
        self.incident_engine = MissionIncidentCommandEngine()
        self.task_engine = MissionTaskEngine()
        self.sla_engine = MissionSLAEngine()
        self.blocker_engine = MissionBlockerEngine()
        self.workflow_orchestrator = MissionWorkflowOrchestrator()
        self.integration_bridge = SubsystemIntegrationBridge()
        self.copilot_bridge = CopilotMissionControlBridge()
        self.streamer = RealtimeStateStreamer()
        self.health_engine = MissionControlHealthEngine()
        self.conflict_engine = StateConflictResolutionEngine()

    def get_mission_overview(self, tenant_id: str = "default_tenant") -> Dict[str, Any]:
        state = self.state_engine.get_unified_state(tenant_id)
        posture = self.posture_engine.evaluate_posture()
        health = self.health_engine.check_health()
        tasks = self.task_engine.list_tasks()
        workflows = self.workflow_orchestrator.list_workflows()

        return {
            "tenant_id": tenant_id,
            "operational_status": "OPERATIONAL",
            "active_threats_count": state.active_threats_count,
            "active_incidents_count": state.active_incidents_count,
            "pending_tasks_count": len(tasks),
            "running_workflows_count": len([w for w in workflows if w.status == "RUNNING"]),
            "state_conflicts_count": len(self.conflict_engine.list_conflicts()),
            "overall_posture_score": posture.threat_posture,
            "posture_trend": posture.overall_trend,
            "system_health": health.overall_health,
            "evaluated_at": datetime.now(timezone.utc).isoformat(),
        }
