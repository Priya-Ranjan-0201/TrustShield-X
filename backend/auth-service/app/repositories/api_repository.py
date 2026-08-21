"""Async API Repository Layer (Phase 3.7 Part 1A.16).

Provides database operations for persisting and retrieving api_catalog,
api_capabilities, api_usage, api_frameworks, api_statistics, api_cross_reference,
library_inventory, and framework_inventory.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.api_intelligence import (
    APIModel,
    APICapabilityModel,
    APIUsageModel,
    APIFrameworkModel,
    APIStatisticModel,
    APICrossRefModel,
    LibraryInventoryModel,
    FrameworkInventoryModel,
)
from app.schemas.api_intelligence_models import APIIntelligenceResultDTO


class APIRepository:
    """Async repository for API Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_api_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: APIIntelligenceResultDTO,
    ) -> APIStatisticModel:
        """Saves API catalog, capabilities, usage, frameworks, libraries, xrefs, and statistics inside one atomic transaction."""
        for entry in dto.api_catalog:
            self.db.add(
                APIModel(
                    scan_id=scan_id,
                    canonical_id=entry.canonical_id,
                    package_name=entry.package_name,
                    class_name=entry.class_name,
                    method_name=entry.method_name,
                    signature=entry.signature,
                    framework=entry.framework,
                    min_sdk=entry.min_sdk,
                    deprecated=entry.deprecated,
                )
            )

        for cap in dto.capabilities:
            self.db.add(
                APICapabilityModel(
                    scan_id=scan_id,
                    api_canonical_id=cap.api_canonical_id,
                    capability=cap.capability.value if hasattr(cap.capability, "value") else str(cap.capability),
                )
            )

        for usage in dto.api_usage:
            self.db.add(
                APIUsageModel(
                    scan_id=scan_id,
                    caller_method=usage.caller_method,
                    api_canonical_id=usage.api_canonical_id,
                    offset=usage.offset,
                )
            )

        for fw in dto.frameworks:
            self.db.add(
                APIFrameworkModel(
                    scan_id=scan_id,
                    framework_name=fw.framework_name,
                    version=fw.version,
                    detected_by=fw.detected_by,
                )
            )

        for lib in dto.libraries:
            self.db.add(
                LibraryInventoryModel(
                    scan_id=scan_id,
                    library_name=lib.library_name,
                    version=lib.version,
                    package_prefix=lib.package_prefix,
                )
            )

        for xref in dto.xrefs:
            self.db.add(
                APICrossRefModel(
                    scan_id=scan_id,
                    source_symbol=xref.source_symbol,
                    api_canonical_id=xref.api_canonical_id,
                    xref_type=xref.xref_type,
                )
            )

        stats_m = APIStatisticModel(
            scan_id=scan_id,
            total_apis=dto.statistics.total_apis,
            unique_frameworks=dto.statistics.unique_frameworks,
            most_used_capability=dto.statistics.most_used_capability,
        )
        self.db.add(stats_m)

        await self.db.commit()
        return stats_m

    async def get_api_intelligence(self, scan_id: uuid.UUID) -> Optional[APIStatisticModel]:
        stmt = select(APIStatisticModel).where(APIStatisticModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
