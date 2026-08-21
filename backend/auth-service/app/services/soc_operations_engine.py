"""SOC Operations Engine Master Facade (Phase 4.0 Part 7 — Section 1).

Coordinates alert ingestion, correlation, incident lifecycle, automated triage, SLA management,
playbook execution, four-eyes approvals, simulation, empirical verification, and rollback.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.schemas.soc_operations_models import (
    SOCAlertDTO,
    AlertClusterDTO,
    SecurityIncidentDTO,
    TriageResultDTO,
    IncidentTimelineEventDTO,
    IncidentAssignmentDTO,
    IncidentSLADTO,
    ResponsePlaybookDTO,
    ResponseActionDTO,
    ApprovalRequestDTO,
    ResponseSimulationDTO,
    ResponseExecutionDTO,
    ResponseVerificationDTO,
    ResponseRollbackDTO,
    EvidenceCollectionRecordDTO,
    AlertSourceLiteral,
    IncidentPriorityLiteral,
    ApprovalStatusLiteral,
)
from app.services.soc.alert_normalization_engine import AlertNormalizationEngine
from app.services.soc.alert_correlation_engine import SOCAlertCorrelationEngine
from app.services.soc.incident_creation_engine import IncidentCreationEngine
from app.services.soc.incident_triage_engine import IncidentTriageEngine
from app.services.soc.incident_enrichment_engine import IncidentEnrichmentEngine
from app.services.soc.incident_timeline_engine import IncidentTimelineEngine, SLAEngine
from app.services.soc.response_playbook_engine import ResponsePlaybookEngine
from app.services.soc.approval_engine import ApprovalEngine
from app.services.soc.response_simulation_engine import ResponseSimulationEngine
from app.services.soc.response_execution_engine import ResponseExecutionEngine
from app.services.soc.rollback_engine import RollbackEngine
from app.services.soc.response_verification_engine import ResponseVerificationEngine
from app.services.soc.evidence_collection_engine import EvidenceCollectionEngine


from app.services.soc.response_adapters import (
    DNSResponseAdapter,
    FirewallResponseAdapter,
    EDRResponseAdapter,
)


class SOCOperationsEngine:
    """Master facade for TruthShield X Security Operations Center intelligence and SOAR automation."""

    def __init__(self):
        self.normalizer = AlertNormalizationEngine()
        self.correlation_engine = SOCAlertCorrelationEngine()
        self.incident_engine = IncidentCreationEngine()
        self.triage_engine = IncidentTriageEngine()
        self.enrichment_engine = IncidentEnrichmentEngine()
        self.timeline_engine = IncidentTimelineEngine()
        self.sla_engine = SLAEngine()
        self.playbook_engine = ResponsePlaybookEngine()
        self.approval_engine = ApprovalEngine()
        
        dns_adapter = DNSResponseAdapter()
        firewall_adapter = FirewallResponseAdapter()
        edr_adapter = EDRResponseAdapter()
        self._shared_adapters = {
            "BLOCK_DOMAIN": dns_adapter,
            "BLOCK_URL": dns_adapter,
            "BLOCK_IP": firewall_adapter,
            "UPDATE_FIREWALL_RULE": firewall_adapter,
            "ISOLATE_DEVICE": edr_adapter,
            "QUARANTINE_FILE": edr_adapter,
        }

        self.simulation_engine = ResponseSimulationEngine()
        self.execution_engine = ResponseExecutionEngine(adapters=self._shared_adapters)
        self.rollback_engine = RollbackEngine(adapters=self._shared_adapters)
        self.verification_engine = ResponseVerificationEngine(adapters=self._shared_adapters)
        self.evidence_engine = EvidenceCollectionEngine()
        self._alerts: Dict[str, SOCAlertDTO] = {}
        self._actions: Dict[str, ResponseActionDTO] = {}

    def ingest_and_process_alert(
        self,
        raw_alert: Dict[str, Any],
        source_system: AlertSourceLiteral = "INTERNAL_DETECTOR",
        organization_id: Optional[str] = None,
    ) -> Tuple[SOCAlertDTO, SecurityIncidentDTO]:
        """Ingest, normalize, correlate, and cluster an alert into an incident (Sections 1, 2, 6, 11)."""
        # 1. Normalize
        alert = self.normalizer.normalize_alert(raw_alert, source_system, organization_id)
        self._alerts[alert.alert_id] = alert

        # 2. Correlate with existing alerts
        cluster = self.correlation_engine.correlate_alert(alert, list(self._alerts.values()))

        # 3. Create or update Security Incident
        incident = self.incident_engine.create_or_update_incident_from_alert(alert, cluster)

        # 4. Record Timeline Event
        self.timeline_engine.add_event(
            incident_id=incident.incident_id,
            event_type="ALERT_CORRELATED" if incident.source_alert_count > 1 else "INCIDENT_CREATED",
            description=f"Alert '{alert.title}' correlated into incident {incident.incident_number}",
            entity_ids=alert.entity_ids,
            alert_id=alert.alert_id,
        )

        return alert, incident

    def triage_incident(self, incident_id: str) -> TriageResultDTO:
        incident = self.incident_engine.get_incident(incident_id)
        if not incident:
            raise KeyError(f"Incident {incident_id} not found.")

        related_alerts = [a for a in self._alerts.values() if a.incident_id == incident_id]
        triage_res = self.triage_engine.triage_incident(incident, related_alerts)

        self.timeline_engine.add_event(
            incident_id=incident.incident_id,
            event_type="TRIAGE_COMPLETED",
            description=f"Automated triage assessment generated for {incident.incident_number}",
        )
        return triage_res

    def assign_incident(self, incident_id: str, analyst_id: str, assigned_by: str = "SOC_LEAD") -> SecurityIncidentDTO:
        incident = self.incident_engine.get_incident(incident_id)
        if not incident:
            raise KeyError(f"Incident {incident_id} not found.")

        incident.owner_id = analyst_id
        incident.status = "ASSIGNED"

        self.timeline_engine.add_event(
            incident_id=incident.incident_id,
            event_type="ANALYST_ASSIGNED",
            description=f"Incident assigned to analyst {analyst_id}",
            actor=assigned_by,
        )
        return incident

    def create_response_action(
        self,
        incident_id: str,
        action_type: str,
        target: str,
        requested_by: str,
        reason: str,
        requires_approval: bool = True,
    ) -> Tuple[ResponseActionDTO, Optional[ApprovalRequestDTO]]:
        incident = self.incident_engine.get_incident(incident_id)
        if not incident:
            raise KeyError(f"Incident {incident_id} not found.")

        action = ResponseActionDTO(
            incident_id=incident_id,
            action_type=action_type,
            target=target,
            requested_by=requested_by,
            reason=reason,
            approval_status="PENDING" if requires_approval else "NOT_REQUIRED",
            status="WAITING_APPROVAL" if requires_approval else "QUEUED",
        )
        self._actions[action.action_id] = action

        approval = None
        if requires_approval:
            approval = self.approval_engine.create_approval_request(
                action=action,
                requested_by=requested_by,
                reason=reason,
                risk=incident.severity,
            )
            self.timeline_engine.add_event(
                incident_id=incident_id,
                event_type="APPROVAL_REQUESTED",
                description=f"Approval requested for action {action_type} on target {target}",
                actor=requested_by,
                action_id=action.action_id,
            )

        return action, approval

    def approve_action(self, approval_id: str, approver_id: str, reason: str = "Approved by SOC Lead") -> ResponseActionDTO:
        appr = self.approval_engine.decide_approval(
            approval_id=approval_id,
            approver_id=approver_id,
            decision="APPROVED",
            decision_reason=reason,
        )
        action = self._actions.get(appr.action_id)
        if action:
            action.approval_status = "APPROVED"
            action.approved_by = approver_id
            action.status = "QUEUED"
            self.timeline_engine.add_event(
                incident_id=action.incident_id,
                event_type="APPROVED",
                description=f"Action {action.action_type} approved by {approver_id}",
                actor=approver_id,
                action_id=action.action_id,
            )
        return action

    def reject_action(self, approval_id: str, approver_id: str, reason: str = "Rejected by SOC Lead") -> ResponseActionDTO:
        appr = self.approval_engine.decide_approval(
            approval_id=approval_id,
            approver_id=approver_id,
            decision="REJECTED",
            decision_reason=reason,
        )
        action = self._actions.get(appr.action_id)
        if action:
            action.approval_status = "REJECTED"
            action.status = "CANCELLED"
            self.timeline_engine.add_event(
                incident_id=action.incident_id,
                event_type="REJECTED",
                description=f"Action {action.action_type} rejected by {approver_id}: {reason}",
                actor=approver_id,
                action_id=action.action_id,
            )
        return action

    def execute_action(self, action_id: str) -> Tuple[ResponseActionDTO, ResponseExecutionDTO, ResponseVerificationDTO]:
        action = self._actions.get(action_id)
        if not action:
            raise KeyError(f"Action {action_id} not found.")

        # Execute through execution engine
        action, exec_dto = self.execution_engine.execute_action(action)

        # Verify through verification engine
        action, ver_dto = self.verification_engine.verify_action(action)

        self.timeline_engine.add_event(
            incident_id=action.incident_id,
            event_type="ACTION_COMPLETED" if action.status == "COMPLETED" else "ACTION_FAILED",
            description=f"Action {action.action_type} executed: {action.status}",
            action_id=action.action_id,
        )

        return action, exec_dto, ver_dto

    def rollback_action(self, action_id: str, executed_by: str = "SOC_LEAD") -> Tuple[ResponseActionDTO, ResponseRollbackDTO]:
        action = self._actions.get(action_id)
        if not action:
            raise KeyError(f"Action {action_id} not found.")

        action, rol_dto = self.rollback_engine.execute_rollback(action, executed_by=executed_by)

        self.timeline_engine.add_event(
            incident_id=action.incident_id,
            event_type="ROLLBACK_COMPLETED" if action.status == "ROLLED_BACK" else "ACTION_FAILED",
            description=f"Rollback {action.action_type} result: {rol_dto.rollback_status}",
            actor=executed_by,
            action_id=action.action_id,
        )
        return action, rol_dto

    def list_alerts(self) -> List[SOCAlertDTO]:
        return list(self._alerts.values())

    def list_incidents(self) -> List[SecurityIncidentDTO]:
        return self.incident_engine.list_incidents()

    def get_incident(self, incident_id: str) -> Optional[SecurityIncidentDTO]:
        return self.incident_engine.get_incident(incident_id)
