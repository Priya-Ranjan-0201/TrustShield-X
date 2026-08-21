"""SQLAlchemy 2.0 ORM Models for Trust Narrative Engine (Phase 4.0 Part 2 — Section 47-48).

Defines database models for 10 narrative tables:
trust_narratives, narrative_sections, narrative_statements, narrative_lineage,
narrative_versions, narrative_templates, narrative_validation_results,
narrative_generation_runs, narrative_generation_errors, narrative_translation_records.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class TrustNarrativeModel(Base):
    __tablename__ = "trust_narratives"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False, default="4.0.0")
    template_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    mode: Mapped[str] = mapped_column(String(32), nullable=False, default="DETERMINISTIC_MODE")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="COMPLETED", index=True)
    json_document: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeSectionModel(Base):
    __tablename__ = "narrative_sections"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    section_id: Mapped[str] = mapped_column(String(128), nullable=False)
    title: Mapped[str] = mapped_column(String(256), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeStatementModel(Base):
    __tablename__ = "narrative_statements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    statement_id: Mapped[str] = mapped_column(String(128), nullable=False)
    statement_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    claim: Mapped[str] = mapped_column(Text, nullable=False)
    claim_strength: Mapped[str] = mapped_column(String(32), nullable=False, default="SUPPORTED")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeLineageModel(Base):
    __tablename__ = "narrative_lineage"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    statement_id: Mapped[str] = mapped_column(String(128), nullable=False)
    report_id: Mapped[str] = mapped_column(String(128), nullable=False)
    section_id: Mapped[str] = mapped_column(String(128), nullable=False)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_id: Mapped[str] = mapped_column(String(128), nullable=False)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    risk_factor_id: Mapped[str] = mapped_column(String(128), nullable=False, default="")
    generated_by: Mapped[str] = mapped_column(String(128), nullable=False, default="TrustNarrativeEngine")
    template_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeVersionModel(Base):
    __tablename__ = "narrative_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    schema_version: Mapped[str] = mapped_column(String(64), nullable=False)
    template_version: Mapped[str] = mapped_column(String(64), nullable=False)
    language_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    change_reason: Mapped[str] = mapped_column(String(256), nullable=False, default="INITIAL_GENERATION")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeTemplateModel(Base):
    __tablename__ = "narrative_templates"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    template_type: Mapped[str] = mapped_column(String(64), nullable=False)
    template_content: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeValidationModel(Base):
    __tablename__ = "narrative_validation_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    validation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    checks_performed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    checks_passed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    checks_failed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    failure_details: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeGenerationRunModel(Base):
    __tablename__ = "narrative_generation_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False)
    analysis_id: Mapped[str] = mapped_column(String(128), nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="SUCCESS")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeGenerationErrorModel(Base):
    __tablename__ = "narrative_generation_errors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    error_code: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False)
    error_message: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class NarrativeTranslationModel(Base):
    __tablename__ = "narrative_translation_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    narrative_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    source_language: Mapped[str] = mapped_column(String(16), nullable=False, default="en")
    target_language: Mapped[str] = mapped_column(String(16), nullable=False)
    translated_document: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
