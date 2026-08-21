"""SQLAlchemy 2.0 ORM Models for Automated Digital Trust Report Generator (Phase 4.0 Part 1).

Defines database models for 11 report tables:
digital_trust_reports, report_sections, report_findings, report_evidence,
report_recommendations, report_provenance, report_lineage, report_versions,
report_generation_runs, report_generation_errors, report_metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class DigitalTrustReportModel(Base):
    __tablename__ = "digital_trust_reports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False, default="4.0.0")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED", index=True)
    report_type: Mapped[str] = mapped_column(String(64), nullable=False, default="FULL_TRUST_REPORT")
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_band: Mapped[str] = mapped_column(String(32), nullable=False, default="TRUSTED")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    evidence_sufficiency: Mapped[str] = mapped_column(String(32), nullable=False, default="SUFFICIENT")
    json_document: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportSectionModel(Base):
    __tablename__ = "report_sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    section_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportFindingModel(Base):
    __tablename__ = "report_findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportEvidenceModel(Base):
    __tablename__ = "report_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    card_id: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    observation: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportRecommendationModel(Base):
    __tablename__ = "report_recommendations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    recommendation_text: Mapped[str] = mapped_column(String(512), nullable=False)
    priority: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportProvenanceModel(Base):
    __tablename__ = "report_provenance"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    statement_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportLineageModel(Base):
    __tablename__ = "report_lineage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    section_id: Mapped[str] = mapped_column(String(128), nullable=False)
    statement_text: Mapped[str] = mapped_column(String(512), nullable=False)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False)
    original_source: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportVersionModel(Base):
    __tablename__ = "report_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_version: Mapped[str] = mapped_column(String(64), nullable=False)
    change_reason: Mapped[str] = mapped_column(String(256), nullable=False, default="INITIAL_GENERATION")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportGenerationRunModel(Base):
    __tablename__ = "report_generation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="SUCCESS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportGenerationErrorModel(Base):
    __tablename__ = "report_generation_errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    error_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False)
    error_message: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReportMetricModel(Base):
    __tablename__ = "report_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reports_generated_total: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    reports_failed_total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
