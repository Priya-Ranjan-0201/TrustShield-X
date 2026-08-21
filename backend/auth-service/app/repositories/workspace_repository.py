"""Async Workspace Repository Layer (Phase 3.7 Part 1A.4).

Provides database persistence operations for apk_workspace, workspace_files, and workspace_statistics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_workspace import WorkspaceModel, WorkspaceFileModel, WorkspaceStatisticsModel
from app.services.apk_workspace_manager import APKWorkspaceResult


class WorkspaceRepository:
    """Async repository for workspace, file inventory, and statistics DB persistence."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_workspace(
        self,
        scan_id: uuid.UUID,
        workspace_id: str,
        apk_sha256: str,
        workspace_path: str,
        status: str = "READY_FOR_STATIC_ANALYSIS",
    ) -> WorkspaceModel:
        model = WorkspaceModel(
            workspace_id=workspace_id,
            scan_id=scan_id,
            apk_sha256=apk_sha256,
            workspace_path=workspace_path,
            status=status,
        )
        self.db.add(model)
        await self.db.flush()
        return model

    async def save_full_workspace(
        self,
        scan_id: uuid.UUID,
        workspace_res: APKWorkspaceResult,
    ) -> WorkspaceModel:
        """Saves workspace root record, all inventory file rows, and statistics inside one transaction."""
        root_model = await self.create_workspace(
            scan_id=scan_id,
            workspace_id=workspace_res.workspace_id,
            apk_sha256=workspace_res.apk_sha256,
            workspace_path=workspace_res.workspace_path,
            status=workspace_res.status,
        )

        # Bulk insert file entries
        file_models = [
            WorkspaceFileModel(
                workspace_id=root_model.id,
                relative_path=entry.relative_path,
                mime_type=entry.mime_type,
                sha256=entry.sha256,
                size=entry.size,
                entropy=entry.entropy,
                category=entry.category,
            )
            for entry in workspace_res.inventory.entries
        ]
        if file_models:
            self.db.add_all(file_models)

        # Insert statistics summary
        stats = workspace_res.inventory.categories_summary
        stats_model = WorkspaceStatisticsModel(
            workspace_id=root_model.id,
            file_count=workspace_res.inventory.total_files,
            directory_count=workspace_res.inventory.total_directories,
            dex_count=stats.get("DEX", 0),
            library_count=stats.get("NATIVE_LIBRARY", 0),
            asset_count=stats.get("JSON", 0),
            resource_count=stats.get("IMAGE", 0) + stats.get("XML", 0),
            binary_count=stats.get("BINARY", 0),
            xml_count=stats.get("XML", 0),
            certificate_count=stats.get("CERTIFICATE", 0),
        )
        self.db.add(stats_model)

        await self.db.commit()
        return root_model

    async def get_workspace(self, scan_id: uuid.UUID) -> Optional[WorkspaceModel]:
        stmt = (
            select(WorkspaceModel)
            .where(WorkspaceModel.scan_id == scan_id)
            .options(
                selectinload(WorkspaceModel.files),
                selectinload(WorkspaceModel.statistics),
            )
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, scan_id: uuid.UUID) -> bool:
        stmt = select(WorkspaceModel.id).where(WorkspaceModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none() is not None

    async def delete_workspace(self, scan_id: uuid.UUID) -> bool:
        model = await self.get_workspace(scan_id)
        if not model:
            return False

        await self.db.delete(model)
        await self.db.commit()
        return True
