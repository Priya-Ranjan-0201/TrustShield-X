"""Async Database Repository for Enterprise Governance (Phase 4.0 Part 8 — Section 85).

Handles all database persistence for organizations, users, roles, policies, legal holds,
retention, exports, audit events, compliance, sessions, and API keys.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.governance import (
    OrganizationModel,
    OrganizationUserModel,
    RoleModel,
    RoleVersionModel,
    PermissionModel,
    GovernancePolicyModel,
    PolicyVersionModel,
    RetentionPolicyModel,
    LegalHoldModel,
    DeletionRequestModel,
    PrivacyRequestModel,
    DataExportModel,
    AuditEventModel,
    AuditIntegrityCheckpointModel,
    GovernanceAlertModel,
    ComplianceFrameworkModel,
    ComplianceControlModel,
    ComplianceEvidenceModel,
    ComplianceAssessmentModel,
    UserSessionModel,
    ServiceAccountModel,
    APIKeyModel,
)


class GovernanceRepository:
    """Async database repository for enterprise governance control plane."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_organization(self, model: OrganizationModel) -> OrganizationModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_organization(self, org_id: str) -> Optional[OrganizationModel]:
        stmt = select(OrganizationModel).where(OrganizationModel.organization_id == org_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_user(self, model: OrganizationUserModel) -> OrganizationUserModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_user(self, user_id: str) -> Optional[OrganizationUserModel]:
        stmt = select(OrganizationUserModel).where(OrganizationUserModel.user_id == user_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_organization_users(self, organization_id: str) -> List[OrganizationUserModel]:
        stmt = select(OrganizationUserModel).where(OrganizationUserModel.organization_id == organization_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_role(self, model: RoleModel) -> RoleModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_role(self, role_id: str) -> Optional[RoleModel]:
        stmt = select(RoleModel).where(RoleModel.role_id == role_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_roles(self, organization_id: Optional[str] = None) -> List[RoleModel]:
        stmt = select(RoleModel)
        if organization_id:
            stmt = stmt.where((RoleModel.organization_id == organization_id) | (RoleModel.system_role.is_(True)))
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_policy(self, model: GovernancePolicyModel) -> GovernancePolicyModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_policy(self, policy_id: str) -> Optional[GovernancePolicyModel]:
        stmt = select(GovernancePolicyModel).where(GovernancePolicyModel.policy_id == policy_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def list_policies(self, organization_id: str) -> List[GovernancePolicyModel]:
        stmt = select(GovernancePolicyModel).where(GovernancePolicyModel.organization_id == organization_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_legal_hold(self, model: LegalHoldModel) -> LegalHoldModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_legal_holds(self, organization_id: str) -> List[LegalHoldModel]:
        stmt = select(LegalHoldModel).where(LegalHoldModel.organization_id == organization_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_deletion_request(self, model: DeletionRequestModel) -> DeletionRequestModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def create_privacy_request(self, model: PrivacyRequestModel) -> PrivacyRequestModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_privacy_requests(self, organization_id: str) -> List[PrivacyRequestModel]:
        stmt = select(PrivacyRequestModel).where(PrivacyRequestModel.organization_id == organization_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_data_export(self, model: DataExportModel) -> DataExportModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def get_data_export(self, export_id: str) -> Optional[DataExportModel]:
        stmt = select(DataExportModel).where(DataExportModel.export_id == export_id)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_audit_event(self, model: AuditEventModel) -> AuditEventModel:
        self.session.add(model)
        await self.session.commit()
        return model

    async def list_audit_events(self, organization_id: str, limit: int = 100) -> List[AuditEventModel]:
        stmt = select(AuditEventModel).where(AuditEventModel.organization_id == organization_id).order_by(AuditEventModel.timestamp.desc()).limit(limit)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())

    async def create_api_key(self, model: APIKeyModel) -> APIKeyModel:
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model

    async def list_api_keys(self, organization_id: str) -> List[APIKeyModel]:
        stmt = select(APIKeyModel).where(APIKeyModel.organization_id == organization_id)
        res = await self.session.execute(stmt)
        return list(res.scalars().all())
