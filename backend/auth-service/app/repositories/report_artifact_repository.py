"""Repository for Report Artifact & Rendering Operations (Phase 4.0 Part 3 — Section 69).

Provides async CRUD queries across all 10 rendering tables:
artifacts, jobs, signatures, integrity, manifests, storage records, runs, errors,
validations, and download audits.
"""

import json
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.report_rendering import (
    ReportArtifactModel,
    ReportExportJobModel,
    ReportSignatureModel,
    ReportIntegrityModel,
    ReportManifestModel,
    ArtifactStorageModel,
    ReportRenderingRunModel,
    ReportRenderingErrorModel,
    ReportFormatValidationModel,
    ReportDownloadAuditModel,
)
from app.schemas.report_rendering_models import (
    ReportArtifactDTO,
    ReportExportJobDTO,
    ReportSignatureDTO,
    ReportManifestDTO,
    ReportIntegrityRecordDTO,
    ReportFormatValidationDTO,
)


class ReportArtifactRepository:
    """Async repository for Report Rendering persistence and retrieval."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_artifact(self, dto: ReportArtifactDTO) -> ReportArtifactModel:
        model = ReportArtifactModel(
            artifact_id=dto.artifact_id,
            report_id=dto.report_id,
            analysis_id=dto.analysis_id,
            report_version=dto.report_version,
            artifact_version=dto.artifact_version,
            format=dto.format,
            mime_type=dto.mime_type,
            file_extension=dto.file_extension,
            size_bytes=dto.size_bytes,
            sha256=dto.sha256,
            content_encoding=dto.content_encoding,
            renderer_name=dto.renderer_name,
            renderer_version=dto.renderer_version,
            schema_version=dto.schema_version,
            generated_at=dto.generated_at,
            generation_duration_ms=dto.generation_duration_ms,
            storage_location=dto.storage_location,
            status=dto.status,
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def get_artifact_by_id(self, artifact_id: str) -> Optional[ReportArtifactModel]:
        res = await self.db.execute(
            select(ReportArtifactModel).where(ReportArtifactModel.artifact_id == artifact_id)
        )
        scalars = res.scalars()
        item = scalars.first() if hasattr(scalars, "first") else None
        if hasattr(item, "__await__"):
            item = await item
        return item

    async def get_artifacts_by_report_id(self, report_id: str) -> List[ReportArtifactModel]:
        res = await self.db.execute(
            select(ReportArtifactModel).where(ReportArtifactModel.report_id == report_id)
        )
        scalars = res.scalars()
        items = scalars.all() if hasattr(scalars, "all") else []
        if hasattr(items, "__await__"):
            items = await items
        return list(items)

    async def store_integrity(self, dto: ReportIntegrityRecordDTO) -> ReportIntegrityModel:
        model = ReportIntegrityModel(
            integrity_id=dto.integrity_id,
            report_id=dto.report_id,
            artifact_id=dto.artifact_id,
            content_hash=dto.content_hash,
            artifact_hash=dto.artifact_hash,
            is_valid=dto.is_valid,
            verified_at=dto.verified_at,
            detected_tampering=dto.detected_tampering,
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def store_signature(self, dto: ReportSignatureDTO) -> ReportSignatureModel:
        model = ReportSignatureModel(
            signature_id=dto.signature_id,
            artifact_id=dto.artifact_id,
            algorithm=dto.algorithm,
            key_id=dto.key_id,
            signature=dto.signature,
            signed_hash=dto.signed_hash,
            signed_at=dto.signed_at,
            status=dto.status,
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def store_manifest(self, dto: ReportManifestDTO) -> ReportManifestModel:
        model = ReportManifestModel(
            report_id=dto.report_id,
            analysis_id=dto.analysis_id,
            report_version=dto.report_version,
            artifact_id=dto.artifact_id,
            artifact_format=dto.artifact_format,
            artifact_sha256=dto.artifact_sha256,
            content_sha256=dto.content_sha256,
            manifest_json=json.dumps(dto.model_dump(), indent=2),
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def create_export_job(self, dto: ReportExportJobDTO) -> ReportExportJobModel:
        model = ReportExportJobModel(
            job_id=dto.job_id,
            report_id=dto.report_id,
            format=dto.format,
            status=dto.status,
            progress=dto.progress,
            requested_by=dto.requested_by,
            started_at=dto.started_at,
            completed_at=dto.completed_at,
            artifact_id=dto.artifact_id,
            error_code=dto.error_code,
        )
        self.db.add(model)
        await self.db.commit()
        return model

    async def get_export_job(self, job_id: str) -> Optional[ReportExportJobModel]:
        res = await self.db.execute(
            select(ReportExportJobModel).where(ReportExportJobModel.job_id == job_id)
        )
        scalars = res.scalars()
        item = scalars.first() if hasattr(scalars, "first") else None
        if hasattr(item, "__await__"):
            item = await item
        return item

    async def store_download_audit(self, artifact_id: str, user_id: str, ip_address: str = "127.0.0.1") -> ReportDownloadAuditModel:
        audit_id = f"audit_{artifact_id}_{int(datetime.now(timezone.utc).timestamp())}"
        model = ReportDownloadAuditModel(
            audit_id=audit_id,
            artifact_id=artifact_id,
            user_id=user_id,
            ip_address=ip_address,
        )
        self.db.add(model)
        await self.db.commit()
        return model
