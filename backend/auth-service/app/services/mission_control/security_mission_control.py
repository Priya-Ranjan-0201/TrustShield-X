"""
TruthShield X — Security Mission Control

Top-level orchestration layer connecting all TruthShield X capabilities
into a unified Security Mission Control system.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.mission_control_models import (
    MissionControlSummaryDTO,
    IncidentCommandDTO,
    BusinessServiceImpactDTO,
)
from app.services.mission_control.incident_command_engine import IncidentCommandEngine
from app.services.mission_control.crisis_declaration_engine import CrisisDeclarationEngine
from app.services.mission_control.response_plan_engine import ResponsePlanEngine
from app.services.mission_control.crisis_communications_engine import CrisisCommunicationsEngine
from app.services.mission_control.incident_recovery_engine import IncidentRecoveryEngine
from app.services.mission_control.lessons_learned_engine import LessonsLearnedEngine
from app.services.mission_control.crisis_readiness_engine import CrisisReadinessEngine


class SecurityMissionControl:
    """Unified Security Mission Control orchestrator.

    Connects: Signals → Detection → Evidence → Correlation → Incident →
    Crisis Assessment → Digital Twin → Response Planning → Authorization →
    Execution → Verification → Recovery → Lessons Learned.
    """

    def __init__(self):
        self.incident_command = IncidentCommandEngine()
        self.crisis_declaration = CrisisDeclarationEngine()
        self.response_plan = ResponsePlanEngine()
        self.crisis_communications = CrisisCommunicationsEngine()
        self.incident_recovery = IncidentRecoveryEngine()
        self.lessons_learned = LessonsLearnedEngine()
        self.crisis_readiness = CrisisReadinessEngine()

    def get_mission_control_summary(self, tenant_id: str = "default_tenant") -> MissionControlSummaryDTO:
        """Returns aggregated mission control dashboard state."""
        commands = self.incident_command.list_commands(tenant_id)
        active = [c for c in commands if c.command_status not in ("RESOLVED", "CLOSED")]
        critical = [c for c in active if c.severity in ("CRITICAL", "CRISIS")]

        crisis_status = self.crisis_declaration.get_crisis_status(tenant_id)

        readiness = self.crisis_readiness.calculate_readiness(
            detection_readiness=85.0,
            response_readiness=80.0,
            communication_readiness=75.0,
            recovery_readiness=70.0,
            governance_readiness=90.0,
            control_health_readiness=88.0,
            dr_readiness=72.0,
            human_readiness=65.0,
        )

        return MissionControlSummaryDTO(
            active_incidents=len(active),
            critical_alerts=len(critical),
            crisis_status=crisis_status,
            services_at_risk=sum(len(c.affected_service_ids) for c in active),
            pending_response_actions=0,
            approvals_required=0,
            active_recoveries=0,
            residual_risk_score=0.0,
            crisis_readiness=readiness,
        )

    def calculate_blast_radius(
        self,
        command_id: str,
        tenant_id: str = "default_tenant",
    ) -> Dict[str, Any]:
        """Calculates blast radius for an incident. Never marks assets compromised without evidence."""
        cmd = self.incident_command.get_command(command_id, tenant_id)
        if not cmd:
            return {"error": "Incident not found"}

        room = self.incident_command.get_evidence_room(command_id, tenant_id)
        verified_assets = set()
        if room:
            for ev in room.evidence_items:
                if ev.classification == "VERIFIED":
                    verified_assets.update(ev.related_entity_ids)

        return {
            "incident_command_id": command_id,
            "confirmed_affected": list(verified_assets),
            "likely_affected": cmd.affected_asset_ids,
            "potentially_affected": [],
            "unaffected": [],
            "unknown": [],
            "total_confirmed": len(verified_assets),
            "total_likely": len(cmd.affected_asset_ids),
        }

    def assess_business_impact(
        self,
        command_id: str,
        services: Optional[List[Dict[str, Any]]] = None,
        tenant_id: str = "default_tenant",
    ) -> List[BusinessServiceImpactDTO]:
        """Assesses business service impact. Returns UNKNOWN if data unavailable."""
        cmd = self.incident_command.get_command(command_id, tenant_id)
        if not cmd:
            return []

        if not services:
            return [BusinessServiceImpactDTO(
                service_id="unknown",
                service_name="UNKNOWN",
                business_impact_known=False,
            )]

        impacts = []
        for svc in services:
            impact = BusinessServiceImpactDTO(
                service_id=svc.get("service_id", ""),
                service_name=svc.get("service_name", ""),
                owner=svc.get("owner", ""),
                criticality=svc.get("criticality", "UNKNOWN"),
                availability_impact=svc.get("availability_impact", "UNKNOWN"),
                dependency_impact=svc.get("dependency_impact", "UNKNOWN"),
                affected_asset_ids=svc.get("affected_asset_ids", []),
                business_impact_known=True,
            )
            impacts.append(impact)

        return impacts
