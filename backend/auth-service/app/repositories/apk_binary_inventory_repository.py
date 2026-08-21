"""Async APK Binary Inventory Repository Layer (Phase 3.7 Part 1A.12).

Provides database operations for persisting and retrieving apk_binary_inventory,
apk_binary_hashes, and apk_binary_statistics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_binary_inventory import (
    APKBinaryFileModel,
    APKBinaryHashModel,
    APKBinaryStatisticsModel,
)
from app.schemas.apk_binary_inventory_models import APKBinaryInventoryResultDTO


class APKBinaryInventoryRepository:
    """Async repository for APK Binary Inventory DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_binary_inventory(
        self,
        scan_id: uuid.UUID,
        dto: APKBinaryInventoryResultDTO,
    ) -> List[APKBinaryFileModel]:
        """Saves binary entries, hashes, and statistics inside one atomic transaction."""
        file_models: List[APKBinaryFileModel] = []

        for entry in dto.entries:
            f_model = APKBinaryFileModel(
                scan_id=scan_id,
                file_path=entry.file_path,
                filename=entry.filename,
                directory=entry.directory,
                extension=entry.extension,
                file_category=entry.file_category.value if hasattr(entry.file_category, 'value') else str(entry.file_category),
                uncompressed_size=entry.uncompressed_size,
                compressed_size=entry.compressed_size,
                compression_method=entry.compression_method,
                crc32=entry.crc32,
            )
            self.db.add(f_model)
            await self.db.flush()

            h_model = APKBinaryHashModel(
                inventory_id=f_model.id,
                sha256=entry.hashes.sha256,
                sha1=entry.hashes.sha1,
                md5=entry.hashes.md5,
                crc32=entry.hashes.crc32,
                entropy=entry.hashes.entropy,
                mime_type=entry.hashes.mime_type,
            )
            self.db.add(h_model)
            file_models.append(f_model)

        stats_m = APKBinaryStatisticsModel(
            scan_id=scan_id,
            total_files=dto.statistics.total_files,
            total_directories=dto.statistics.total_directories,
            total_size_bytes=dto.statistics.total_size_bytes,
            compressed_size_bytes=dto.statistics.compressed_size_bytes,
            dex_count=dto.statistics.dex_count,
            native_library_count=dto.statistics.native_library_count,
            assets_count=dto.statistics.assets_count,
            resources_count=dto.statistics.resources_count,
            media_count=dto.statistics.media_count,
            config_count=dto.statistics.config_count,
            unknown_count=dto.statistics.unknown_count,
        )
        self.db.add(stats_m)

        await self.db.commit()
        return file_models

    async def get_inventory(self, scan_id: uuid.UUID) -> List[APKBinaryFileModel]:
        stmt = (
            select(APKBinaryFileModel)
            .where(APKBinaryFileModel.scan_id == scan_id)
            .options(selectinload(APKBinaryFileModel.hashes))
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())
