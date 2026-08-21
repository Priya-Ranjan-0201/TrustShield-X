"""SQLAlchemy 2.0 ORM Models for Unified Trust Intelligence Graph (Phase 4.0 Part 5 — Section 47).

19 tables supporting entities, observations, resolution history, relationships,
evidence bindings, provenance, correlation candidates & runs, threat campaigns,
attack chains, threat actor associations, graph versions, snapshots, and review queue.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    Float,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
    Index,
)
from app.models.base import Base


class CanonicalEntityModel(Base):
    __tablename__ = "intelligence_entities"

    entity_id = Column(String(64), primary_key=True, default=lambda: f"ent_{uuid.uuid4().hex[:12]}")
    entity_type = Column(String(50), nullable=False, index=True)
    canonical_value = Column(Text, nullable=False)
    display_value = Column(Text, nullable=False)
    normalized_value = Column(Text, nullable=False, index=True)
    value_hash = Column(String(64), nullable=False, index=True)
    source_count = Column(Integer, default=1, nullable=False)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    confidence = Column(String(20), default="HIGH", nullable=False, index=True)
    resolution_status = Column(String(30), default="EXACT_MATCH", nullable=False, index=True)
    privacy_classification = Column(String(30), default="PUBLIC", nullable=False)
    organization_id = Column(String(64), nullable=True, index=True)
    entity_metadata = Column("metadata", JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class EntityAliasModel(Base):
    __tablename__ = "entity_aliases"

    alias_id = Column(String(64), primary_key=True, default=lambda: f"al_{uuid.uuid4().hex[:12]}")
    entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    alias_value = Column(Text, nullable=False)
    alias_type = Column(String(50), default="NORMALIZED", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class EntityObservationModel(Base):
    __tablename__ = "entity_observations"

    observation_id = Column(String(64), primary_key=True, default=lambda: f"obs_{uuid.uuid4().hex[:12]}")
    entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    source_analysis_id = Column(String(64), nullable=False, index=True)
    source_module = Column(String(64), nullable=False)
    raw_value = Column(Text, nullable=False)
    observed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    context_data = Column(JSON, default=dict, nullable=False)


class EntityResolutionRecordModel(Base):
    __tablename__ = "entity_resolution_records"

    record_id = Column(String(64), primary_key=True, default=lambda: f"res_{uuid.uuid4().hex[:12]}")
    entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    target_entity_id = Column(String(64), nullable=True, index=True)
    resolution_state = Column(String(30), default="EXACT_MATCH", nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    resolution_method = Column(String(50), default="EXACT_IDENTIFIER", nullable=False)
    signals_used = Column(JSON, default=list, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class IntelligenceRelationshipModel(Base):
    __tablename__ = "intelligence_relationships"

    relationship_id = Column(String(64), primary_key=True, default=lambda: f"rel_{uuid.uuid4().hex[:12]}")
    source_entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    target_entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False, index=True)
    confidence = Column(String(20), default="HIGH", nullable=False, index=True)
    evidence_strength = Column(String(20), default="STRONG", nullable=False)
    resolution_status = Column(String(30), default="ACTIVE", nullable=False, index=True)
    correlation_method = Column(String(50), default="EXACT_IDENTIFIER", nullable=False)
    correlation_version = Column(String(20), default="1.0.0", nullable=False)
    first_observed = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_observed = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    source_count = Column(Integer, default=1, nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    is_manual = Column(Boolean, default=False, nullable=False)
    author_id = Column(String(64), nullable=True)
    staleness_reason = Column(Text, nullable=True)
    conflicting_sources = Column(JSON, default=list, nullable=False)
    relationship_metadata = Column("metadata", JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class RelationshipEvidenceModel(Base):
    __tablename__ = "relationship_evidence"

    evidence_binding_id = Column(String(64), primary_key=True, default=lambda: f"rev_{uuid.uuid4().hex[:12]}")
    relationship_id = Column(String(64), ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True)
    evidence_id = Column(String(64), nullable=False, index=True)
    finding_id = Column(String(64), nullable=True, index=True)
    analysis_id = Column(String(64), nullable=False, index=True)
    evidence_strength = Column(String(20), default="DIRECT", nullable=False)
    observation_summary = Column(Text, nullable=False)


class RelationshipProvenanceModel(Base):
    __tablename__ = "relationship_provenance"

    provenance_id = Column(String(64), primary_key=True, default=lambda: f"rpr_{uuid.uuid4().hex[:12]}")
    relationship_id = Column(String(64), ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True)
    source_system = Column(String(64), nullable=False)
    rule_id = Column(String(64), nullable=False)
    rule_version = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CorrelationCandidateModel(Base):
    __tablename__ = "correlation_candidates"

    candidate_id = Column(String(64), primary_key=True, default=lambda: f"cand_{uuid.uuid4().hex[:12]}")
    source_entity_id = Column(String(64), nullable=False, index=True)
    target_entity_id = Column(String(64), nullable=False, index=True)
    relationship_type = Column(String(50), nullable=False)
    candidate_score = Column(Float, default=0.0, nullable=False)
    confidence = Column(String(20), default="MEDIUM", nullable=False)
    evidence_count = Column(Integer, default=1, nullable=False)
    correlation_method = Column(String(50), default="NORMALIZED_IDENTIFIER", nullable=False)
    false_correlation_penalty = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CorrelationRunModel(Base):
    __tablename__ = "intelligence_correlation_runs"

    run_id = Column(String(64), primary_key=True, default=lambda: f"crun_{uuid.uuid4().hex[:12]}")
    case_id = Column(String(64), nullable=True, index=True)
    analysis_scope = Column(JSON, default=list, nullable=False)
    correlation_version = Column(String(20), default="1.0.0", nullable=False)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="RUNNING", nullable=False)
    candidate_count = Column(Integer, default=0, nullable=False)
    accepted_count = Column(Integer, default=0, nullable=False)
    rejected_count = Column(Integer, default=0, nullable=False)
    uncertain_count = Column(Integer, default=0, nullable=False)
    error_count = Column(Integer, default=0, nullable=False)


class ThreatCampaignModel(Base):
    __tablename__ = "threat_campaigns"

    campaign_id = Column(String(64), primary_key=True, default=lambda: f"camp_{uuid.uuid4().hex[:12]}")
    name = Column(String(255), nullable=False, index=True)
    campaign_type = Column(String(50), default="PHISHING_CAMPAIGN", nullable=False, index=True)
    status = Column(String(20), default="ACTIVE", nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    first_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    entity_count = Column(Integer, default=0, nullable=False)
    analysis_count = Column(Integer, default=0, nullable=False)
    finding_count = Column(Integer, default=0, nullable=False)
    evidence_count = Column(Integer, default=0, nullable=False)
    relationship_count = Column(Integer, default=0, nullable=False)
    threat_actor = Column(String(128), default="UNKNOWN", nullable=False)
    threat_actor_confidence = Column(String(50), default="UNCONFIRMED_ASSOCIATION", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class CampaignEntityModel(Base):
    __tablename__ = "campaign_entities"

    id = Column(String(64), primary_key=True, default=lambda: f"ce_{uuid.uuid4().hex[:12]}")
    campaign_id = Column(String(64), ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True)
    entity_id = Column(String(64), ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True)


class CampaignRelationshipModel(Base):
    __tablename__ = "campaign_relationships"

    id = Column(String(64), primary_key=True, default=lambda: f"cr_{uuid.uuid4().hex[:12]}")
    campaign_id = Column(String(64), ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True)
    relationship_id = Column(String(64), ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True)


class AttackChainModel(Base):
    __tablename__ = "attack_chains"

    chain_id = Column(String(64), primary_key=True, default=lambda: f"chain_{uuid.uuid4().hex[:12]}")
    case_id = Column(String(64), nullable=True, index=True)
    campaign_id = Column(String(64), ForeignKey("threat_campaigns.campaign_id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    entry_point = Column(Text, nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    status = Column(String(20), default="ACTIVE", nullable=False)
    evidence_ids = Column(JSON, default=list, nullable=False)
    finding_ids = Column(JSON, default=list, nullable=False)
    missing_steps_count = Column(Integer, default=0, nullable=False)
    uncertainty_summary = Column(Text, default="", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class AttackChainStepModel(Base):
    __tablename__ = "attack_chain_steps"

    step_id = Column(String(64), primary_key=True, default=lambda: f"step_{uuid.uuid4().hex[:12]}")
    chain_id = Column(String(64), ForeignKey("attack_chains.chain_id", ondelete="CASCADE"), nullable=False, index=True)
    step_number = Column(Integer, nullable=False)
    stage = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    step_state = Column(String(30), default="CONFIRMED_STEP", nullable=False)
    confidence = Column(String(20), default="HIGH", nullable=False)
    entity_ids = Column(JSON, default=list, nullable=False)
    evidence_ids = Column(JSON, default=list, nullable=False)
    finding_ids = Column(JSON, default=list, nullable=False)
    missing_evidence_note = Column(Text, nullable=True)


class ThreatActorAssociationModel(Base):
    __tablename__ = "threat_actor_associations"

    association_id = Column(String(64), primary_key=True, default=lambda: f"taa_{uuid.uuid4().hex[:12]}")
    actor_name = Column(String(128), nullable=False, index=True)
    campaign_id = Column(String(64), ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True)
    confidence = Column(String(20), default="LOW", nullable=False)
    source = Column(String(64), default="THREAT_INTEL", nullable=False)
    evidence = Column(Text, default="", nullable=False)
    attribution_type = Column(String(50), default="UNCONFIRMED_ASSOCIATION", nullable=False)
    attribution_status = Column(String(30), default="UNCONFIRMED", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class GraphVersionModel(Base):
    __tablename__ = "graph_versions"

    graph_version_id = Column(String(64), primary_key=True, default=lambda: f"gver_{uuid.uuid4().hex[:12]}")
    case_id = Column(String(64), nullable=True, index=True)
    version_number = Column(Integer, default=1, nullable=False)
    schema_version = Column(String(20), default="4.0.0", nullable=False)
    correlation_version = Column(String(20), default="1.0.0", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    created_by = Column(String(64), default="SYSTEM", nullable=False)
    change_summary = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=False)


class GraphSnapshotModel(Base):
    __tablename__ = "graph_snapshots"

    snapshot_id = Column(String(64), primary_key=True, default=lambda: f"gsnap_{uuid.uuid4().hex[:12]}")
    graph_version_id = Column(String(64), ForeignKey("graph_versions.graph_version_id", ondelete="CASCADE"), nullable=False, index=True)
    case_id = Column(String(64), nullable=True, index=True)
    snapshot_data = Column(JSON, default=dict, nullable=False)
    total_nodes = Column(Integer, default=0, nullable=False)
    total_edges = Column(Integer, default=0, nullable=False)
    content_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class GraphChangeModel(Base):
    __tablename__ = "graph_changes"

    change_id = Column(String(64), primary_key=True, default=lambda: f"gchg_{uuid.uuid4().hex[:12]}")
    graph_version_id = Column(String(64), ForeignKey("graph_versions.graph_version_id", ondelete="CASCADE"), nullable=False, index=True)
    change_type = Column(String(50), nullable=False)  # ENTITY_ADDED, RELATIONSHIP_ADDED, CONFIDENCE_CHANGED, etc.
    target_id = Column(String(64), nullable=False)
    details = Column(JSON, default=dict, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CorrelationReviewQueueModel(Base):
    __tablename__ = "correlation_review_queue"

    review_id = Column(String(64), primary_key=True, default=lambda: f"revq_{uuid.uuid4().hex[:12]}")
    relationship_id = Column(String(64), ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True)
    source_entity_value = Column(Text, nullable=False)
    target_entity_value = Column(Text, nullable=False)
    relationship_type = Column(String(50), nullable=False)
    confidence = Column(String(20), nullable=False)
    flag_reason = Column(String(50), nullable=False)
    priority = Column(String(20), default="MEDIUM", nullable=False)
    status = Column(String(20), default="PENDING", nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
