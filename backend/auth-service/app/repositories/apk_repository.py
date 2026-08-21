"""Async Database Repository for AI Android APK Security Engine (Phase 3.7 Part 1A Message 3B).

Exposes typed DTO methods for APK metadata, permissions, DEX inventory, native libraries, and certificates.
Uses selectinload() to avoid N+1 queries. Zero SQL in controllers.
"""

import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func, update
from sqlalchemy.orm import selectinload

from app.models.apk_metadata import (
    APKMetadataModel,
    APKPermissionModel,
    APKDEXModel,
    APKNativeLibraryModel,
    APKCertificateModel,
)
from app.models.scan_history import ScanHistory
from app.schemas.apk_models import (
    APKMetadata,
    ManifestMetadata,
    PermissionInfo,
    DEXSummary,
    DEXMetadata,
    NativeLibrarySummary,
    NativeLibraryMetadata,
)
from app.services.certificate_extractor import CertificateMetadata


class APKRepository:
    """Production Async Database Repository for APK Security Records."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def save_apk_analysis(
        self,
        scan_id: uuid.UUID,
        apk_meta: APKMetadata,
        cert_meta: Optional[CertificateMetadata] = None,
    ) -> APKMetadataModel:
        """Persists complete APK metadata, permissions, DEX, native libraries, and certificates inside one atomic transaction."""
        try:
            root_model = APKMetadataModel(
                scan_id=scan_id,
                package_name=apk_meta.package_name,
                version_name=apk_meta.version_name,
                version_code=apk_meta.version_code,
                application_label=apk_meta.application_label,
                min_sdk=apk_meta.min_sdk,
                target_sdk=apk_meta.target_sdk,
                compile_sdk=apk_meta.compile_sdk,
                apk_size=apk_meta.package_size,
                apk_sha256=apk_meta.apk_sha256,
                parsed_successfully=True,
            )
            self.db.add(root_model)
            await self.db.flush()

            if apk_meta.manifest_metadata and apk_meta.manifest_metadata.permissions:
                await self.create_permissions(root_model.id, apk_meta.manifest_metadata.permissions)

            if apk_meta.dex_summary and apk_meta.dex_summary.dex_files:
                await self.create_dex_inventory(root_model.id, apk_meta.dex_summary.dex_files)

            if apk_meta.native_library_summary and apk_meta.native_library_summary.libraries:
                await self.create_native_libraries(root_model.id, apk_meta.native_library_summary.libraries)

            if cert_meta and not cert_meta.certificate_unavailable and cert_meta.sha256:
                await self.create_certificates(root_model.id, cert_meta)

            await self.db.commit()
            await self.db.refresh(root_model)
            return root_model
        except Exception as e:
            await self.db.rollback()
            raise e

    async def create_apk_metadata(self, scan_id: uuid.UUID, apk_meta: APKMetadata) -> APKMetadataModel:
        """Creates root APK metadata record."""
        root = APKMetadataModel(
            scan_id=scan_id,
            package_name=apk_meta.package_name,
            version_name=apk_meta.version_name,
            version_code=apk_meta.version_code,
            application_label=apk_meta.application_label,
            min_sdk=apk_meta.min_sdk,
            target_sdk=apk_meta.target_sdk,
            compile_sdk=apk_meta.compile_sdk,
            apk_size=apk_meta.package_size,
            apk_sha256=apk_meta.apk_sha256,
            parsed_successfully=True,
        )
        self.db.add(root)
        await self.db.flush()
        return root

    async def create_permissions(self, apk_id: uuid.UUID, permissions: List[PermissionInfo]) -> List[APKPermissionModel]:
        """Bulk inserts permission records."""
        models = [
            APKPermissionModel(
                apk_id=apk_id,
                permission_name=p.name,
                protection_level=p.protection_level,
                declared_by_app=p.declared_by_app,
            )
            for p in permissions
        ]
        self.db.add_all(models)
        await self.db.flush()
        return models

    async def create_dex_inventory(self, apk_id: uuid.UUID, dex_files: List[DEXMetadata]) -> List[APKDEXModel]:
        """Bulk inserts DEX file inventory records."""
        models = [
            APKDEXModel(
                apk_id=apk_id,
                filename=d.filename,
                sha256=d.sha256,
                size=d.size,
                method_count=d.method_count,
                class_count=d.class_count,
            )
            for d in dex_files
        ]
        self.db.add_all(models)
        await self.db.flush()
        return models

    async def create_native_libraries(self, apk_id: uuid.UUID, libraries: List[NativeLibraryMetadata]) -> List[APKNativeLibraryModel]:
        """Bulk inserts native library records."""
        models = [
            APKNativeLibraryModel(
                apk_id=apk_id,
                library_name=lib.library_name,
                architecture=lib.architecture,
                sha256=lib.sha256,
                size=lib.size,
            )
            for lib in libraries
        ]
        self.db.add_all(models)
        await self.db.flush()
        return models

    async def create_certificates(self, apk_id: uuid.UUID, cert_meta: CertificateMetadata) -> APKCertificateModel:
        """Inserts certificate metadata record."""
        cert_model = APKCertificateModel(
            apk_id=apk_id,
            subject=cert_meta.subject,
            issuer=cert_meta.issuer,
            sha256=cert_meta.sha256,
            sha1=cert_meta.sha1,
            signature_algorithm=cert_meta.signature_algorithm,
            public_key_algorithm=cert_meta.public_key_algorithm,
            key_size=cert_meta.public_key_size,
            valid_from=cert_meta.valid_from,
            valid_until=cert_meta.valid_until,
            expired=cert_meta.expired,
            self_signed=cert_meta.self_signed,
        )
        self.db.add(cert_model)
        await self.db.flush()
        return cert_model

    async def get_apk_by_scan(self, scan_id: uuid.UUID) -> Optional[APKMetadataModel]:
        """Retrieves stored APK metadata with selectinload relationships by scan ID."""
        stmt = (
            select(APKMetadataModel)
            .where(APKMetadataModel.scan_id == scan_id)
            .options(
                selectinload(APKMetadataModel.permissions),
                selectinload(APKMetadataModel.dex_files),
                selectinload(APKMetadataModel.native_libraries),
                selectinload(APKMetadataModel.certificates),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def get_apk_by_sha256(self, sha256: str) -> Optional[APKMetadataModel]:
        """Retrieves stored APK metadata by SHA-256 hash."""
        stmt = (
            select(APKMetadataModel)
            .where(APKMetadataModel.apk_sha256 == sha256)
            .options(
                selectinload(APKMetadataModel.permissions),
                selectinload(APKMetadataModel.dex_files),
                selectinload(APKMetadataModel.native_libraries),
                selectinload(APKMetadataModel.certificates),
            )
        )
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()

    async def list_user_apks(self, user_id: uuid.UUID, limit: int = 20, offset: int = 0) -> List[APKMetadataModel]:
        """Lists user's stored APK metadata records with pagination."""
        stmt = (
            select(APKMetadataModel)
            .join(ScanHistory, APKMetadataModel.scan_id == ScanHistory.id)
            .where(ScanHistory.user_id == user_id)
            .order_by(APKMetadataModel.created_at.desc())
            .limit(limit)
            .offset(offset)
            .options(selectinload(APKMetadataModel.certificates))
        )
        res = await self.db.execute(stmt)
        return list(res.scalars().all())

    async def delete_apk(self, apk_id: uuid.UUID) -> bool:
        """Deletes an APK metadata record by APK ID (cascades permissions, dex, libs, certs)."""
        stmt = delete(APKMetadataModel).where(APKMetadataModel.id == apk_id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.rowcount > 0

    async def delete_by_scan(self, scan_id: uuid.UUID) -> bool:
        """Deletes stored APK records by scan ID."""
        stmt = delete(APKMetadataModel).where(APKMetadataModel.scan_id == scan_id)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.rowcount > 0

    async def exists_sha256(self, sha256: str) -> bool:
        """Checks if an APK SHA-256 hash already exists in storage."""
        stmt = select(func.count(APKMetadataModel.id)).where(APKMetadataModel.apk_sha256 == sha256)
        res = await self.db.execute(stmt)
        return (res.scalar() or 0) > 0

    async def exists_package(self, package_name: str) -> bool:
        """Checks if a package name exists in storage."""
        stmt = select(func.count(APKMetadataModel.id)).where(APKMetadataModel.package_name == package_name)
        res = await self.db.execute(stmt)
        return (res.scalar() or 0) > 0

    async def update_processing_status(self, apk_id: uuid.UUID, status: bool) -> bool:
        """Updates the parsed_successfully processing status of an APK record."""
        stmt = update(APKMetadataModel).where(APKMetadataModel.id == apk_id).values(parsed_successfully=status)
        res = await self.db.execute(stmt)
        await self.db.commit()
        return res.rowcount > 0
