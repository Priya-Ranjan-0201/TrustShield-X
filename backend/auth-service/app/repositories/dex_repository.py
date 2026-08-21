"""Async DEX Repository Layer for DEX & Multi-DEX Intelligence Engine (Phase 3.7 Part 1A.6).

Provides database operations for persisting and retrieving apk_dex_files, apk_dex_classes,
apk_dex_methods, apk_dex_fields, and apk_packages.
"""

import uuid
from typing import Optional, List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.apk_dex import (
    APKDexFileModel,
    APKDexClassModel,
    APKDexMethodModel,
    APKDexFieldModel,
    APKPackageModel,
)
from app.schemas.dex_intelligence_models import MultiDEXIntelligenceDTO


class DEXRepository:
    """Async repository for DEX & Multi-DEX Intelligence DB operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_full_dex_intelligence(
        self,
        scan_id: uuid.UUID,
        dto: MultiDEXIntelligenceDTO,
    ) -> List[APKDexFileModel]:
        """Saves all DEX files, classes, methods, fields, and packages inside one atomic transaction."""
        dex_models: List[APKDexFileModel] = []

        for df in dto.dex_files:
            h = df.header
            dex_file_model = APKDexFileModel(
                scan_id=scan_id,
                dex_name=df.dex_name,
                dex_order=df.dex_order,
                sha256=df.sha256,
                sha1=df.sha1,
                checksum=h.checksum,
                checksum_valid=h.checksum_valid,
                file_size=df.file_size,
                header_size=h.header_size,
                endian_tag=h.endian_tag,
                string_ids_size=h.string_ids_size,
                type_ids_size=h.type_ids_size,
                proto_ids_size=h.proto_ids_size,
                field_ids_size=h.field_ids_size,
                method_ids_size=h.method_ids_size,
                class_defs_size=h.class_defs_size,
            )
            self.db.add(dex_file_model)
            await self.db.flush()

            for cls in df.classes:
                class_model = APKDexClassModel(
                    dex_file_id=dex_file_model.id,
                    class_name=cls.name,
                    package_name=cls.package_name,
                    superclass=cls.superclass,
                    access_flags=cls.access_flags,
                    is_interface=cls.is_interface,
                    is_enum=cls.is_enum,
                    is_abstract=cls.is_abstract,
                    source_file=cls.source_file,
                )
                self.db.add(class_model)
                await self.db.flush()

                for m in cls.methods:
                    method_model = APKDexMethodModel(
                        class_id=class_model.id,
                        method_name=m.name,
                        return_type=m.return_type,
                        parameter_types={"types": m.parameter_types},
                        access_flags=m.access_flags,
                        is_direct=m.is_direct,
                        is_virtual=m.is_virtual,
                        is_native=m.is_native,
                        is_constructor=m.is_constructor,
                    )
                    self.db.add(method_model)

                for f in cls.fields:
                    field_model = APKDexFieldModel(
                        class_id=class_model.id,
                        field_name=f.name,
                        field_type=f.field_type,
                        access_flags=f.access_flags,
                        is_static=f.is_static,
                        is_final=f.is_final,
                    )
                    self.db.add(field_model)

            dex_models.append(dex_file_model)

        # Store Packages
        pkg_models = [
            APKPackageModel(
                scan_id=scan_id,
                package_name=p.package_name,
                class_count=p.class_count,
                depth=p.depth,
            )
            for p in dto.packages
        ]
        if pkg_models:
            self.db.add_all(pkg_models)

        await self.db.commit()
        return dex_models

    async def get_dex_intelligence(self, scan_id: uuid.UUID) -> List[APKDexFileModel]:
        stmt = (
            select(APKDexFileModel)
            .where(APKDexFileModel.scan_id == scan_id)
            .options(
                selectinload(APKDexFileModel.classes).selectinload(APKDexClassModel.methods),
                selectinload(APKDexFileModel.classes).selectinload(APKDexClassModel.fields),
            )
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def delete_dex_intelligence(self, scan_id: uuid.UUID) -> bool:
        models = await self.get_dex_intelligence(scan_id)
        if not models:
            return False

        for m in models:
            await self.db.delete(m)
        await self.db.commit()
        return True
