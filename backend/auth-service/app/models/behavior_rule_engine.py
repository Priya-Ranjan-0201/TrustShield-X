"""SQLAlchemy 2.0 ORM Models for Enterprise Malware Behavior Pattern & Rule Evaluation Engine (Phase 3.9 Part 1A.24).

Defines database models for 13 rule engine tables:
behavior_rules, behavior_rule_versions, behavior_rule_packs, behavior_rule_dependencies,
behavior_rule_conditions, behavior_rule_evaluations, behavior_rule_condition_results,
behavior_rule_execution_traces, behavior_rule_evidence, behavior_rule_suppressions,
behavior_rule_exceptions, behavior_rule_conflicts, behavior_rule_metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class BehaviorRuleModel(Base):
    __tablename__ = "behavior_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    namespace: Mapped[str] = mapped_column(String(64), nullable=False, default="DATAFLOW")
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    severity_hint: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    confidence_hint: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleVersionModel(Base):
    __tablename__ = "behavior_rule_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    author: Mapped[str] = mapped_column(String(128), nullable=False, default="TruthShield Core Team")
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="ACTIVE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRulePackModel(Base):
    __tablename__ = "behavior_rule_packs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    pack_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    pack_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    rules_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleDependencyModel(Base):
    __tablename__ = "behavior_rule_dependencies"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    depends_on_rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleConditionModel(Base):
    __tablename__ = "behavior_rule_conditions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    condition_id: Mapped[str] = mapped_column(String(128), nullable=False)
    condition_type: Mapped[str] = mapped_column(String(64), nullable=False)
    expected: Mapped[str] = mapped_column(String(256), nullable=False)
    operator: Mapped[str] = mapped_column(String(32), nullable=False, default="AND")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleEvaluationModel(Base):
    __tablename__ = "behavior_rule_evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evaluation_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    namespace: Mapped[str] = mapped_column(String(64), nullable=False)
    state: Mapped[str] = mapped_column(String(32), nullable=False, default="MATCHED", index=True)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    evidence_provenance: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleConditionResultModel(Base):
    __tablename__ = "behavior_rule_condition_results"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    condition_id: Mapped[str] = mapped_column(String(128), nullable=False)
    condition_type: Mapped[str] = mapped_column(String(64), nullable=False)
    expected: Mapped[str] = mapped_column(String(256), nullable=False)
    actual: Mapped[str] = mapped_column(String(256), nullable=False)
    matched: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    reason: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleExecutionTraceModel(Base):
    __tablename__ = "behavior_rule_execution_traces"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    trace_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_version: Mapped[str] = mapped_column(String(64), nullable=False)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    final_state: Mapped[str] = mapped_column(String(32), nullable=False, default="MATCHED")
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleEvidenceModel(Base):
    __tablename__ = "behavior_rule_evidence"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    evidence_type: Mapped[str] = mapped_column(String(64), nullable=False)
    source_module: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleSuppressionModel(Base):
    __tablename__ = "behavior_rule_suppressions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    suppression_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleExceptionModel(Base):
    __tablename__ = "behavior_rule_exceptions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    exception_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_id: Mapped[str] = mapped_column(String(128), nullable=False)
    scope: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleConflictModel(Base):
    __tablename__ = "behavior_rule_conflicts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    rule_a_id: Mapped[str] = mapped_column(String(128), nullable=False)
    rule_b_id: Mapped[str] = mapped_column(String(128), nullable=False)
    reason: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class BehaviorRuleMetricModel(Base):
    __tablename__ = "behavior_rule_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    rules_loaded: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_evaluated: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_matched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_partially_matched: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_not_evaluable: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_suppressed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_conflicted: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
