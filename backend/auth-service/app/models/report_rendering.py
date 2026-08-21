"""SQLAlchemy 2.0 ORM Models for Report Rendering, Export & Secure Delivery (Phase 4.0 Part 3 — Section 68).

Defines database models for 10 rendering tables:
report_artifacts, report_export_jobs, report_signatures, report_integrity_records,
report_manifests, artifact_storage_records, report_rendering_runs,
report_rendering_errors, report_format_validations, report_download_audits.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class ReportArtifactModel(Base):
    __tablename__ = "report_artifacts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    artifact_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    format: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    file_extension: Mapped[str] = mapped_column(String(16), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    content_encoding: Mapped[str] = mapped_column(String(32), nullable=False, default="utf-8")
    renderer_name: Mapped[str] = mapped_column(String(128), nullable=False)
    renderer_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False, default="4.0.0")
    generated_at: Mapped[str] = mapped_column(String(64), nullable=False)
    generation_duration_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    storage_location: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportExportJobModel(Base):
    __tablename__ = "report_export_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED", index=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=100)
    requested_by: Mapped[str] = mapped_column(String(128), nullable=False, default="system")
    started_at: Mapped[str] = mapped_column(String(64), nullable=True)
    completed_at: Mapped[str] = mapped_column(String(64), nullable=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=True)
    error_code: Mapped[str] = mapped_column(String(64), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportSignatureModel(Base):
    __tablename__ = "report_signatures"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signature_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    algorithm: Mapped[str] = mapped_column(String(64), nullable=False, default="Ed25519")
    key_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    signature: Mapped[str] = mapped_column(Text, nullable=False, default="")
    signed_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    signed_at: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="NOT_SIGNED")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportIntegrityModel(Base):
    __tablename__ = "report_integrity_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    integrity_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    artifact_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    verified_at: Mapped[str] = mapped_column(String(64), nullable=False)
    detected_tampering: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportManifestModel(Base):
    __tablename__ = "report_manifests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_format: Mapped[str] = mapped_column(String(32), nullable=False)
    artifact_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    content_sha256: Mapped[str] = mapped_column(String(64), nullable=False)
    manifest_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ArtifactStorageModel(Base):
    __tablename__ = "artifact_storage_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    storage_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    provider: Mapped[str] = mapped_column(String(64), nullable=False, default="LOCAL")
    bucket_or_path: Mapped[str] = mapped_column(String(512), nullable=False)
    object_key: Mapped[str] = mapped_column(String(256), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportRenderingRunModel(Base):
    __tablename__ = "report_rendering_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False)
    format: Mapped[str] = mapped_column(String(32), nullable=False)
    duration_ms: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="SUCCESS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportRenderingErrorModel(Base):
    __tablename__ = "report_rendering_errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    error_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    error_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    error_message: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportFormatValidationModel(Base):
    __tablename__ = "report_format_validations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    validation_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    formats_tested: Mapped[str] = mapped_column(String(256), nullable=False, default="[]")
    consistent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    discrepancies: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportDownloadAuditModel(Base):
    __tablename__ = "report_download_audits"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    audit_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    artifact_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(String(128), nullable=False, default="anonymous")
    ip_address: Mapped[str] = mapped_column(String(64), nullable=False, default="127.0.0.1")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
