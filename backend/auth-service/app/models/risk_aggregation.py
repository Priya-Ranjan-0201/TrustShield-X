"""SQLAlchemy 2.0 ORM Models for Enterprise Risk Aggregation Engine (Phase 3.9 Part 1B).

Defines database models for 13 risk tables:
risk_assessments, risk_factors, risk_category_scores, risk_contributions,
risk_interactions, risk_mitigations, risk_protective_factors, risk_contradictions,
risk_audit_records, risk_policy_versions, risk_policy_rules, risk_decision_records, risk_metrics.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base


class RiskAssessmentModel(Base):
    __tablename__ = "risk_assessments"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    assessment_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0, index=True)
    risk_band: Mapped[str] = mapped_column(String(32), nullable=False, default="TRUSTED", index=True)
    confidence_level: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    evidence_sufficiency: Mapped[str] = mapped_column(String(32), nullable=False, default="SUFFICIENT")
    decision_state: Mapped[str] = mapped_column(String(32), nullable=False, default="TRUSTED", index=True)
    primary_risk_category: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK_THREAT")
    risk_factor_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    supporting_finding_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    contradictory_finding_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    mitigating_factor_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    protective_factor_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    uncertainty_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    engine_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    configuration_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskFactorModel(Base):
    __tablename__ = "risk_factors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    factor_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False, default="NETWORK_THREAT")
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    base_contribution: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    final_contribution: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    confidence: Mapped[str] = mapped_column(String(32), nullable=False, default="HIGH")
    evidence_sufficiency: Mapped[str] = mapped_column(String(32), nullable=False, default="SUFFICIENT")
    reason: Mapped[str] = mapped_column(String(512), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskCategoryScoreModel(Base):
    __tablename__ = "risk_category_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    raw_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    normalized_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    risk_band: Mapped[str] = mapped_column(String(32), nullable=False, default="LOW_RISK")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskContributionModel(Base):
    __tablename__ = "risk_contributions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    finding_id: Mapped[str] = mapped_column(String(128), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    contribution_weight: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskInteractionModel(Base):
    __tablename__ = "risk_interactions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    interaction_id: Mapped[str] = mapped_column(String(128), nullable=False)
    factor_a_id: Mapped[str] = mapped_column(String(128), nullable=False)
    factor_b_id: Mapped[str] = mapped_column(String(128), nullable=False)
    amplification_bonus: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskMitigationModel(Base):
    __tablename__ = "risk_mitigations"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    mitigation_id: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    reduction_amount: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskProtectiveFactorModel(Base):
    __tablename__ = "risk_protective_factors"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    protective_id: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    reduction_amount: Mapped[float] = mapped_column(Float, nullable=False, default=5.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskContradictionModel(Base):
    __tablename__ = "risk_contradictions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    contradiction_id: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    uncertainty_penalty: Mapped[float] = mapped_column(Float, nullable=False, default=2.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskAuditRecordModel(Base):
    __tablename__ = "risk_audit_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    audit_id: Mapped[str] = mapped_column(String(128), nullable=False)
    policy_version: Mapped[str] = mapped_column(String(64), nullable=False, default="1.0.0")
    configuration_checksum: Mapped[str] = mapped_column(String(128), nullable=False)
    audit_trail_text: Mapped[str] = mapped_column(String(1024), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskPolicyVersionModel(Base):
    __tablename__ = "risk_policy_versions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_version: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    author: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskPolicyRuleModel(Base):
    __tablename__ = "risk_policy_rules"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    policy_version: Mapped[str] = mapped_column(String(64), nullable=False)
    rule_name: Mapped[str] = mapped_column(String(128), nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=10.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskDecisionRecordModel(Base):
    __tablename__ = "risk_decision_records"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    decision_id: Mapped[str] = mapped_column(String(128), nullable=False)
    decision_state: Mapped[str] = mapped_column(String(32), nullable=False, default="TRUSTED")
    recommendation: Mapped[str] = mapped_column(String(64), nullable=False, default="ANALYSIS_COMPLETE")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class RiskMetricModel(Base):
    __tablename__ = "risk_metrics"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scan_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=False, index=True)
    assessments_evaluated: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    high_risk_assessments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    critical_risk_assessments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    insufficient_evidence_assessments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
