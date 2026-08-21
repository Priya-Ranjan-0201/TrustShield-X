"""Async Permission Repository Layer for Permission Intelligence Normalization Engine (Phase 3.7 Part 1A.8).

Provides database operations for persisting and retrieving permission_catalog, apk_permission_intelligence,
permission_relationships, and permission_sdk_support.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_permission_intel import (
    PermissionCatalogModel,
    APKPermissionIntelligenceModel,
    PermissionRelationshipModel,
    PermissionSDKSupportModel,
)
from app.schemas.permission_intelligence_models import PermissionIntelligenceResultDTO


class PermissionRepository:
    """Async repository for Permission Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_permission_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: PermissionIntelligenceResultDTO,
    ) -> List[APKPermissionIntelligenceModel]:
        """Saves all normalized permission records inside one atomic transaction."""
        models: List[APKPermissionIntelligenceModel] = [
            APKPermissionIntelligenceModel(
                scan_id=scan_id,
                permission_name=p.permission_name,
                category=p.category,
                protection_level=p.protection_level,
                permission_group=p.permission_group,
                is_runtime=p.is_runtime,
                is_dangerous=p.is_dangerous,
                is_custom=p.is_custom,
                is_vendor=p.is_vendor,
                is_unknown=p.is_unknown,
                target_sdk_supported=p.target_sdk_supported,
            )
            for p in dto.permissions
        ]

        if models:
            self.db.add_all(models)
            await self.db.commit()

        return models

    async def get_permissions(self, scan_id: uuid.UUID) -> List[APKPermissionIntelligenceModel]:
        stmt = select(APKPermissionIntelligenceModel).where(APKPermissionIntelligenceModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def delete_permissions(self, scan_id: uuid.UUID) -> bool:
        permissions = await self.get_permissions(scan_id)
        if not permissions:
            return False

        for p in permissions:
            await self.db.delete(p)
        await self.db.commit()
        return True
