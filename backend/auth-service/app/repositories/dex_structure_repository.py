"""Async DEX Structure Repository Layer (Phase 3.7 Part 1A.13).

Provides database operations for persisting and retrieving dex_packages,
dex_classes, dex_methods, dex_fields, dex_strings, dex_types, and dex_statistics.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dex_structure import (
    DEXPackageModel,
    DEXClassModel,
    DEXMethodModel,
    DEXFieldModel,
    DEXStringModel,
    DEXTypeModel,
    DEXStatisticsModel,
)
from app.schemas.dex_structure_models import DEXStructureResultDTO


class DEXStructureRepository:
    """Async repository for DEX Structure DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_dex_structure(
        self,
        scan_id: uuid.UUID,
        dto: DEXStructureResultDTO,
    ) -> DEXStatisticsModel:
        """Saves packages, classes, methods, fields, strings, types, and statistics inside one atomic transaction."""
        for p in dto.packages:
            self.db.add(
                DEXPackageModel(
                    scan_id=scan_id,
                    package_name=p.package_name,
                    parent_package=p.parent_package,
                    depth=p.depth,
                    class_count=p.class_count,
                    method_count=p.method_count,
                )
            )

        for c in dto.classes:
            self.db.add(
                DEXClassModel(
                    scan_id=scan_id,
                    class_name=c.full_name,
                    simple_name=c.simple_name,
                    package_name=c.package_name,
                    superclass=c.superclass,
                    interfaces=c.interfaces,
                    access_flags=c.access_flags,
                    is_abstract=c.is_abstract,
                    is_final=c.is_final,
                    is_inner=c.is_inner,
                    source_file=c.source_file,
                )
            )

        for m in dto.methods:
            self.db.add(
                DEXMethodModel(
                    scan_id=scan_id,
                    class_name=m.class_name,
                    method_name=m.method_name,
                    return_type=m.return_type,
                    parameter_types=m.parameter_types,
                    access_flags=m.access_flags,
                    is_constructor=m.is_constructor,
                    is_static=m.is_static,
                    is_native=m.is_native,
                    register_count=m.register_count,
                    instruction_count=m.instruction_count,
                )
            )

        for f in dto.fields:
            self.db.add(
                DEXFieldModel(
                    scan_id=scan_id,
                    class_name=f.class_name,
                    field_name=f.field_name,
                    field_type=f.field_type,
                    access_flags=f.access_flags,
                    is_static=f.is_static,
                    is_final=f.is_final,
                )
            )

        for s in dto.strings[:5000]:  # Limit top 5000 strings to keep DB insert performant
            self.db.add(
                DEXStringModel(
                    scan_id=scan_id,
                    string_value=s.string_value,
                    string_hash=s.string_hash,
                    length=s.length,
                    offset=s.offset,
                )
            )

        for t in dto.types:
            self.db.add(
                DEXTypeModel(
                    scan_id=scan_id,
                    type_name=t.type_name,
                    kind=t.kind,
                )
            )

        stats_m = DEXStatisticsModel(
            scan_id=scan_id,
            total_packages=dto.statistics.total_packages,
            total_classes=dto.statistics.total_classes,
            total_methods=dto.statistics.total_methods,
            total_fields=dto.statistics.total_fields,
            total_strings=dto.statistics.total_strings,
            avg_methods_per_class=dto.statistics.avg_methods_per_class,
            largest_package=dto.statistics.largest_package,
            largest_class=dto.statistics.largest_class,
        )
        self.db.add(stats_m)

        await self.db.commit()
        return stats_m

    async def get_structure(self, scan_id: uuid.UUID) -> Optional[DEXStatisticsModel]:
        stmt = select(DEXStatisticsModel).where(DEXStatisticsModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
