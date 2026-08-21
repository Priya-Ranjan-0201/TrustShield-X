"""Repository for Continuous Intelligence & Real-Time Monitoring (Phase 4.0 Part 6 — Section 83).

Handles all database persistence operations outside controllers.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.continuous_intelligence import (
    ThreatFeedConfigurationModel,
    ThreatFeedHealthModel,
    ThreatFeedVersionModel,
    IntelligenceObservationModel,
    IntelligenceStateChangeModel,
    MonitoringJobModel,
    MonitoringJobRunModel,
    IntelligenceEventModel,
    EventProcessingRecordModel,
    EventDeadLetterModel,
    SecurityAlertModel,
    AlertFingerprintModel,
    AlertSuppressionModel,
    AlertAcknowledgementModel,
    AlertEscalationModel,
    NotificationPolicyModel,
    NotificationDeliveryModel,
    IntelligenceReassessmentModel,
    RiskAssessmentVersionModel,
    SecurityIncidentModel,
    ReportUpdateEventModel,
    RealtimeSubscriptionModel,
)


class ContinuousIntelligenceRepository:
    """Async database repository for continuous intelligence."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_feed(self, model: ThreatFeedConfigurationModel) -> ThreatFeedConfigurationModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_feed(self, feed_id: str) -> Optional[ThreatFeedConfigurationModel]:
        stmt = select(ThreatFeedConfigurationModel).where(ThreatFeedConfigurationModel.feed_id == feed_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_feeds(self, enabled_only: bool = False) -> List[ThreatFeedConfigurationModel]:
        stmt = select(ThreatFeedConfigurationModel)
        if enabled_only:
            stmt = stmt.where(ThreatFeedConfigurationModel.enabled.is_(True))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def store_feed_health(self, health: ThreatFeedHealthModel) -> ThreatFeedHealthModel:
        self.session.add(health)
        await self.session.commit()
        return health

    async def store_observation(self, obs: IntelligenceObservationModel) -> IntelligenceObservationModel:
        self.session.add(obs)
        await self.session.commit()
        return obs

    async def store_event(self, evt: IntelligenceEventModel) -> IntelligenceEventModel:
        self.session.add(evt)
        await self.session.commit()
        return evt

    async def create_alert(self, alert: SecurityAlertModel) -> SecurityAlertModel:
        self.session.add(alert)
        await self.session.commit()
        await self.session.refresh(alert)
        return alert

    async def get_alert(self, alert_id: str) -> Optional[SecurityAlertModel]:
        stmt = select(SecurityAlertModel).where(SecurityAlertModel.alert_id == alert_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_alerts(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        case_id: Optional[str] = None,
        limit: int = 50,
    ) -> List[SecurityAlertModel]:
        stmt = select(SecurityAlertModel)
        if status:
            stmt = stmt.where(SecurityAlertModel.status == status)
        if priority:
            stmt = stmt.where(SecurityAlertModel.priority == priority)
        if case_id:
            stmt = stmt.where(SecurityAlertModel.case_id == case_id)
        stmt = stmt.order_by(SecurityAlertModel.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def store_acknowledgement(self, ack: AlertAcknowledgementModel) -> AlertAcknowledgementModel:
        self.session.add(ack)
        await self.session.commit()
        return ack

    async def store_escalation(self, esc: AlertEscalationModel) -> AlertEscalationModel:
        self.session.add(esc)
        await self.session.commit()
        return esc

    async def store_suppression(self, supp: AlertSuppressionModel) -> AlertSuppressionModel:
        self.session.add(supp)
        await self.session.commit()
        return supp

    async def store_reassessment(self, reass: IntelligenceReassessmentModel) -> IntelligenceReassessmentModel:
        self.session.add(reass)
        await self.session.commit()
        return reass

    async def store_risk_version(self, rav: RiskAssessmentVersionModel) -> RiskAssessmentVersionModel:
        self.session.add(rav)
        await self.session.commit()
        return rav

    async def store_incident(self, inc: SecurityIncidentModel) -> SecurityIncidentModel:
        self.session.add(inc)
        await self.session.commit()
        await self.session.refresh(inc)
        return inc

    async def list_incidents(self, limit: int = 50) -> List[SecurityIncidentModel]:
        stmt = select(SecurityIncidentModel).order_by(SecurityIncidentModel.created_at.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
