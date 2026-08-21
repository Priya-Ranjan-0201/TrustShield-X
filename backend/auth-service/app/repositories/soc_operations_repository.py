"""Repository for SOC Operations & SOAR Foundation (Phase 4.0 Part 7 — Section 74).

Manages all async database operations for alerts, incidents, playbooks, approvals, and actions outside controllers.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.soc_operations import (
    SOCAlertModel,
    AlertClusterModel,
    SecurityIncidentModel,
    IncidentAlertLinkModel,
    IncidentEntityLinkModel,
    IncidentFindingLinkModel,
    IncidentEvidenceLinkModel,
    IncidentTimelineModel,
    IncidentAssignmentModel,
    IncidentSLAModel,
    ResponsePlaybookModel,
    ResponsePlaybookVersionModel,
    ResponsePlaybookStepModel,
    ResponseActionModel,
    ResponseApprovalModel,
    ResponseSimulationModel,
    ResponseExecutionModel,
    ResponseVerificationModel,
    ResponseRollbackModel,
    ResponsePolicyModel,
    ResponseProviderRegistryModel,
    EvidenceCollectionRecordModel,
    IncidentMergeModel,
    IncidentSplitModel,
)


class SOCOperationsRepository:
    """Async database repository for SOC intelligence and incident response."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_soc_alert(self, model: SOCAlertModel) -> SOCAlertModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_soc_alert(self, alert_id: str) -> Optional[SOCAlertModel]:
        stmt = select(SOCAlertModel).where(SOCAlertModel.alert_id == alert_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_soc_alerts(
        self,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        incident_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[SOCAlertModel]:
        stmt = select(SOCAlertModel)
        if category:
            stmt = stmt.where(SOCAlertModel.category == category)
        if severity:
            stmt = stmt.where(SOCAlertModel.severity == severity)
        if incident_id:
            stmt = stmt.where(SOCAlertModel.incident_id == incident_id)
        stmt = stmt.order_by(SOCAlertModel.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_incident(self, model: SecurityIncidentModel) -> SecurityIncidentModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_incident(self, incident_id: str) -> Optional[SecurityIncidentModel]:
        stmt = select(SecurityIncidentModel).where(SecurityIncidentModel.incident_id == incident_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_incidents(
        self,
        status: Optional[str] = None,
        severity: Optional[str] = None,
        incident_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[SecurityIncidentModel]:
        stmt = select(SecurityIncidentModel)
        if status:
            stmt = stmt.where(SecurityIncidentModel.status == status)
        if severity:
            stmt = stmt.where(SecurityIncidentModel.severity == severity)
        if incident_type:
            stmt = stmt.where(SecurityIncidentModel.incident_type == incident_type)
        stmt = stmt.order_by(SecurityIncidentModel.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def add_timeline_event(self, model: IncidentTimelineModel) -> IncidentTimelineModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def list_timeline_events(self, incident_id: str) -> List[IncidentTimelineModel]:
        stmt = select(IncidentTimelineModel).where(IncidentTimelineModel.incident_id == incident_id).order_by(IncidentTimelineModel.timestamp.asc())
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_playbook(self, model: ResponsePlaybookModel) -> ResponsePlaybookModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_playbook(self, playbook_id: str) -> Optional[ResponsePlaybookModel]:
        stmt = select(ResponsePlaybookModel).where(ResponsePlaybookModel.playbook_id == playbook_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_playbooks(self) -> List[ResponsePlaybookModel]:
        stmt = select(ResponsePlaybookModel).where(ResponsePlaybookModel.enabled.is_(True))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_action(self, model: ResponseActionModel) -> ResponseActionModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_action(self, action_id: str) -> Optional[ResponseActionModel]:
        stmt = select(ResponseActionModel).where(ResponseActionModel.action_id == action_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_approval(self, model: ResponseApprovalModel) -> ResponseApprovalModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def create_simulation(self, model: ResponseSimulationModel) -> ResponseSimulationModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def create_execution(self, model: ResponseExecutionModel) -> ResponseExecutionModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def create_verification(self, model: ResponseVerificationModel) -> ResponseVerificationModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def create_rollback(self, model: ResponseRollbackModel) -> ResponseRollbackModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def create_evidence_collection(self, model: EvidenceCollectionRecordModel) -> EvidenceCollectionRecordModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def list_incident_evidence(self, incident_id: str) -> List[EvidenceCollectionRecordModel]:
        stmt = select(EvidenceCollectionRecordModel).where(EvidenceCollectionRecordModel.incident_id == incident_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
