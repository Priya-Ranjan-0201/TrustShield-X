"""Async Repository for Digital Trust Investigation Workspace (Phase 4.0 Part 4 — Section 72).

Handles database persistence for workspaces, cases, analyses links, notes,
bookmarks, tasks, shares, annotations, saved views, audit events, and correlations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import json
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.investigation import (
    InvestigationWorkspaceModel,
    InvestigationCaseModel,
    CaseAnalysisModel,
    CaseNoteModel,
    CaseBookmarkModel,
    CaseTaskModel,
    CaseShareModel,
    InvestigationAnnotationModel,
    SavedViewModel,
    SearchHistoryModel,
    InvestigationAuditEventModel,
    InvestigationCorrelationModel,
    WorkspaceStateModel,
)


class InvestigationRepository:
    """Async database repository for investigation workspace objects."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # -----------------------------------------------------------------------
    # Workspace & State Operations
    # -----------------------------------------------------------------------

    async def create_workspace(
        self,
        workspace_id: str,
        title: str,
        analysis_id: str,
        report_id: str,
        user_id: str,
        organization_id: str = "org_default",
        role: str = "ANALYST",
        case_id: Optional[str] = None,
    ) -> InvestigationWorkspaceModel:
        ws = InvestigationWorkspaceModel(
            workspace_id=workspace_id,
            title=title,
            analysis_id=analysis_id,
            report_id=report_id,
            user_id=user_id,
            organization_id=organization_id,
            role=role,
            case_id=case_id,
            status="ACTIVE",
            created_at=datetime.now(timezone.utc),
            last_accessed_at=datetime.now(timezone.utc),
        )
        self.db.add(ws)
        await self.db.commit()
        await self.db.refresh(ws)
        return ws

    async def get_workspace(self, workspace_id: str) -> Optional[InvestigationWorkspaceModel]:
        stmt = select(InvestigationWorkspaceModel).where(InvestigationWorkspaceModel.workspace_id == workspace_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def save_workspace_state(self, state_id: str, workspace_id: str, user_id: str, state_data: Dict[str, Any]) -> WorkspaceStateModel:
        state_json = json.dumps(state_data)
        stmt = select(WorkspaceStateModel).where(WorkspaceStateModel.workspace_id == workspace_id, WorkspaceStateModel.user_id == user_id)
        res = await self.db.execute(stmt)
        existing = res.scalar_one_or_none()

        if existing:
            existing.state_json = state_json
            existing.updated_at = datetime.now(timezone.utc)
            await self.db.commit()
            await self.db.refresh(existing)
            return existing
        else:
            new_state = WorkspaceStateModel(
                state_id=state_id,
                workspace_id=workspace_id,
                user_id=user_id,
                state_json=state_json,
                updated_at=datetime.now(timezone.utc),
            )
            self.db.add(new_state)
            await self.db.commit()
            await self.db.refresh(new_state)
            return new_state

    async def get_workspace_state(self, workspace_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        stmt = select(WorkspaceStateModel).where(WorkspaceStateModel.workspace_id == workspace_id, WorkspaceStateModel.user_id == user_id)
        res = await self.db.execute(stmt)
        record = res.scalar_one_or_none()
        if record:
            return json.loads(record.state_json)
        return None

    # -----------------------------------------------------------------------
    # Case Management Operations
    # -----------------------------------------------------------------------

    async def create_case(
        self,
        case_id: str,
        title: str,
        owner_id: str,
        created_by: str,
        organization_id: str = "org_default",
        description: str = "",
        priority: str = "MEDIUM",
        classification: str = "CONFIDENTIAL",
    ) -> InvestigationCaseModel:
        case = InvestigationCaseModel(
            case_id=case_id,
            organization_id=organization_id,
            title=title,
            description=description,
            status="OPEN",
            priority=priority,
            owner_id=owner_id,
            created_by=created_by,
            classification=classification,
            retention_policy="DEFAULT_30D",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.db.add(case)
        await self.db.commit()
        await self.db.refresh(case)
        return case

    async def get_case(self, case_id: str) -> Optional[InvestigationCaseModel]:
        stmt = select(InvestigationCaseModel).where(InvestigationCaseModel.case_id == case_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list_cases(self, organization_id: str = "org_default", limit: int = 50, offset: int = 0) -> List[InvestigationCaseModel]:
        stmt = (
            select(InvestigationCaseModel)
            .where(InvestigationCaseModel.organization_id == organization_id)
            .order_by(InvestigationCaseModel.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def update_case(self, case_id: str, update_fields: Dict[str, Any]) -> Optional[InvestigationCaseModel]:
        case = await self.get_case(case_id)
        if not case:
            return None
        for k, v in update_fields.items():
            if hasattr(case, k) and v is not None:
                setattr(case, k, v)
        case.updated_at = datetime.now(timezone.utc)
        if update_fields.get("status") in ["CLOSED", "ARCHIVED", "RESOLVED"] and not case.closed_at:
            case.closed_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(case)
        return case

    async def delete_case(self, case_id: str) -> bool:
        stmt = delete(InvestigationCaseModel).where(InvestigationCaseModel.case_id == case_id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.rowcount > 0

    # -----------------------------------------------------------------------
    # Case Analyses Association
    # -----------------------------------------------------------------------

    async def attach_analysis(
        self,
        link_id: str,
        case_id: str,
        analysis_id: str,
        module_type: str,
        target_identifier: str = "",
        risk_score: float = 0.0,
        risk_band: str = "TRUSTED",
    ) -> CaseAnalysisModel:
        link = CaseAnalysisModel(
            link_id=link_id,
            case_id=case_id,
            analysis_id=analysis_id,
            module_type=module_type,
            target_identifier=target_identifier,
            status="COMPLETED",
            risk_score=risk_score,
            risk_band=risk_band,
            attached_at=datetime.now(timezone.utc),
        )
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def get_case_analyses(self, case_id: str) -> List[CaseAnalysisModel]:
        stmt = select(CaseAnalysisModel).where(CaseAnalysisModel.case_id == case_id).order_by(CaseAnalysisModel.attached_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Case Notes Operations
    # -----------------------------------------------------------------------

    async def create_note(
        self,
        note_id: str,
        case_id: str,
        author_id: str,
        content: str,
        note_type: str = "OBSERVATION",
        analysis_id: Optional[str] = None,
        finding_id: Optional[str] = None,
        evidence_id: Optional[str] = None,
        visibility: str = "INTERNAL",
    ) -> CaseNoteModel:
        note = CaseNoteModel(
            note_id=note_id,
            case_id=case_id,
            analysis_id=analysis_id,
            finding_id=finding_id,
            evidence_id=evidence_id,
            author_id=author_id,
            note_type=note_type,
            content=content,
            visibility=visibility,
            status="ACTIVE",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        self.db.add(note)
        await self.db.commit()
        await self.db.refresh(note)
        return note

    async def get_case_notes(self, case_id: str) -> List[CaseNoteModel]:
        stmt = select(CaseNoteModel).where(CaseNoteModel.case_id == case_id).order_by(CaseNoteModel.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_finding_notes(self, finding_id: str) -> List[CaseNoteModel]:
        stmt = select(CaseNoteModel).where(CaseNoteModel.finding_id == finding_id).order_by(CaseNoteModel.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def get_evidence_notes(self, evidence_id: str) -> List[CaseNoteModel]:
        stmt = select(CaseNoteModel).where(CaseNoteModel.evidence_id == evidence_id).order_by(CaseNoteModel.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Bookmarks Operations
    # -----------------------------------------------------------------------

    async def create_bookmark(
        self,
        bookmark_id: str,
        case_id: str,
        user_id: str,
        item_type: str,
        item_id: str,
        label: str = "",
    ) -> CaseBookmarkModel:
        bm = CaseBookmarkModel(
            bookmark_id=bookmark_id,
            case_id=case_id,
            user_id=user_id,
            item_type=item_type,
            item_id=item_id,
            label=label,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(bm)
        await self.db.commit()
        await self.db.refresh(bm)
        return bm

    async def get_case_bookmarks(self, case_id: str, user_id: str) -> List[CaseBookmarkModel]:
        stmt = select(CaseBookmarkModel).where(CaseBookmarkModel.case_id == case_id, CaseBookmarkModel.user_id == user_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Tasks Operations
    # -----------------------------------------------------------------------

    async def create_task(
        self,
        task_id: str,
        case_id: str,
        title: str,
        description: str = "",
        assigned_to: str = "",
        priority: str = "MEDIUM",
        due_at: Optional[datetime] = None,
    ) -> CaseTaskModel:
        task = CaseTaskModel(
            task_id=task_id,
            case_id=case_id,
            title=title,
            description=description,
            assigned_to=assigned_to,
            priority=priority,
            status="TODO",
            due_at=due_at,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_case_tasks(self, case_id: str) -> List[CaseTaskModel]:
        stmt = select(CaseTaskModel).where(CaseTaskModel.case_id == case_id).order_by(CaseTaskModel.created_at.desc())
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Secure Shares Operations
    # -----------------------------------------------------------------------

    async def create_share(
        self,
        share_id: str,
        report_id: str,
        created_by: str,
        expires_at: datetime,
        permission: str = "VIEW_ONLY",
        case_id: Optional[str] = None,
        access_limit: int = 100,
    ) -> CaseShareModel:
        share = CaseShareModel(
            share_id=share_id,
            report_id=report_id,
            case_id=case_id,
            created_by=created_by,
            expires_at=expires_at,
            permission=permission,
            status="ACTIVE",
            access_limit=access_limit,
            access_count=0,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(share)
        await self.db.commit()
        await self.db.refresh(share)
        return share

    async def get_share(self, share_id: str) -> Optional[CaseShareModel]:
        stmt = select(CaseShareModel).where(CaseShareModel.share_id == share_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def revoke_share(self, share_id: str) -> bool:
        stmt = select(CaseShareModel).where(CaseShareModel.share_id == share_id)
        res = await self.db.execute(stmt)
        share = res.scalar_one_or_none()
        if share:
            share.status = "REVOKED"
            share.revoked_at = datetime.now(timezone.utc)
            await self.db.commit()
            return True
        return False

    async def increment_share_access(self, share_id: str) -> bool:
        stmt = select(CaseShareModel).where(CaseShareModel.share_id == share_id)
        res = await self.db.execute(stmt)
        share = res.scalar_one_or_none()
        if share and share.status == "ACTIVE":
            share.access_count += 1
            if share.access_count >= share.access_limit:
                share.status = "EXPIRED"
            await self.db.commit()
            return True
        return False

    # -----------------------------------------------------------------------
    # Annotations & Saved Views
    # -----------------------------------------------------------------------

    async def create_annotation(
        self,
        annotation_id: str,
        target_type: str,
        target_id: str,
        author_id: str,
        tag: str,
        comment: str = "",
    ) -> InvestigationAnnotationModel:
        ann = InvestigationAnnotationModel(
            annotation_id=annotation_id,
            target_type=target_type,
            target_id=target_id,
            author_id=author_id,
            tag=tag,
            comment=comment,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(ann)
        await self.db.commit()
        await self.db.refresh(ann)
        return ann

    async def get_annotations(self, target_id: str) -> List[InvestigationAnnotationModel]:
        stmt = select(InvestigationAnnotationModel).where(InvestigationAnnotationModel.target_id == target_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    # -----------------------------------------------------------------------
    # Correlations & Audit
    # -----------------------------------------------------------------------

    async def create_correlation(
        self,
        correlation_id: str,
        case_id: str,
        source_analysis_id: str,
        target_analysis_id: str,
        source_module: str,
        target_module: str,
        source_finding_id: str,
        target_finding_id: str,
        relationship: str,
        confidence: str = "HIGH",
        evidence_reference: str = "",
    ) -> InvestigationCorrelationModel:
        corr = InvestigationCorrelationModel(
            correlation_id=correlation_id,
            case_id=case_id,
            source_analysis_id=source_analysis_id,
            target_analysis_id=target_analysis_id,
            source_module=source_module,
            target_module=target_module,
            source_finding_id=source_finding_id,
            target_finding_id=target_finding_id,
            relationship=relationship,
            confidence=confidence,
            evidence_reference=evidence_reference,
            created_at=datetime.now(timezone.utc),
        )
        self.db.add(corr)
        await self.db.commit()
        await self.db.refresh(corr)
        return corr

    async def get_correlations(self, case_id: str) -> List[InvestigationCorrelationModel]:
        stmt = select(InvestigationCorrelationModel).where(InvestigationCorrelationModel.case_id == case_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def create_audit_event(
        self,
        event_id: str,
        user_id: str,
        action: str,
        object_type: str,
        object_id: str,
        case_id: Optional[str] = None,
        analysis_id: Optional[str] = None,
        ip_address: str = "127.0.0.1",
    ) -> InvestigationAuditEventModel:
        event = InvestigationAuditEventModel(
            event_id=event_id,
            user_id=user_id,
            action=action,
            object_type=object_type,
            object_id=object_id,
            case_id=case_id,
            analysis_id=analysis_id,
            ip_address=ip_address,
            timestamp=datetime.now(timezone.utc),
        )
        self.db.add(event)
        await self.db.commit()
        await self.db.refresh(event)
        return event

    async def get_audit_events(self, case_id: Optional[str] = None, analysis_id: Optional[str] = None, limit: int = 100) -> List[InvestigationAuditEventModel]:
        query = select(InvestigationAuditEventModel)
        if case_id:
            query = query.where(InvestigationAuditEventModel.case_id == case_id)
        if analysis_id:
            query = query.where(InvestigationAuditEventModel.analysis_id == analysis_id)
        query = query.order_by(InvestigationAuditEventModel.timestamp.desc()).limit(limit)
        res = await self.db.execute(query)
        return list(res.scalars().all())
