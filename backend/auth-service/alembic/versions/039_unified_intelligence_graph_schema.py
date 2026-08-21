"""Alembic Migration 039 — Unified Trust Intelligence Graph Schema (Phase 4.0 Part 5).

Revision ID: 039_unified_intelligence_graph_schema
Revises: 038_investigation_workspace_schema
Create Date: 2026-08-14
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "039_unified_intelligence_graph_schema"
down_revision = "038_investigation_workspace_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. intelligence_entities
    op.create_table(
        "intelligence_entities",
        sa.Column("entity_id", sa.String(64), primary_key=True),
        sa.Column("entity_type", sa.String(50), nullable=False, index=True),
        sa.Column("canonical_value", sa.Text(), nullable=False),
        sa.Column("display_value", sa.Text(), nullable=False),
        sa.Column("normalized_value", sa.Text(), nullable=False, index=True),
        sa.Column("value_hash", sa.String(64), nullable=False, index=True),
        sa.Column("source_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("first_seen", sa.DateTime(), nullable=False, index=True),
        sa.Column("last_seen", sa.DateTime(), nullable=False, index=True),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH", index=True),
        sa.Column("resolution_status", sa.String(30), nullable=False, server_default="EXACT_MATCH", index=True),
        sa.Column("privacy_classification", sa.String(30), nullable=False, server_default="PUBLIC"),
        sa.Column("organization_id", sa.String(64), nullable=True, index=True),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 2. entity_aliases
    op.create_table(
        "entity_aliases",
        sa.Column("alias_id", sa.String(64), primary_key=True),
        sa.Column("entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("alias_value", sa.Text(), nullable=False),
        sa.Column("alias_type", sa.String(50), nullable=False, server_default="NORMALIZED"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 3. entity_observations
    op.create_table(
        "entity_observations",
        sa.Column("observation_id", sa.String(64), primary_key=True),
        sa.Column("entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_analysis_id", sa.String(64), nullable=False, index=True),
        sa.Column("source_module", sa.String(64), nullable=False),
        sa.Column("raw_value", sa.Text(), nullable=False),
        sa.Column("observed_at", sa.DateTime(), nullable=False),
        sa.Column("context_data", sa.JSON(), nullable=False),
    )

    # 4. entity_resolution_records
    op.create_table(
        "entity_resolution_records",
        sa.Column("record_id", sa.String(64), primary_key=True),
        sa.Column("entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target_entity_id", sa.String(64), nullable=True, index=True),
        sa.Column("resolution_state", sa.String(30), nullable=False, server_default="EXACT_MATCH"),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH"),
        sa.Column("resolution_method", sa.String(50), nullable=False, server_default="EXACT_IDENTIFIER"),
        sa.Column("signals_used", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 5. intelligence_relationships
    op.create_table(
        "intelligence_relationships",
        sa.Column("relationship_id", sa.String(64), primary_key=True),
        sa.Column("source_entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("target_entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("relationship_type", sa.String(50), nullable=False, index=True),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH", index=True),
        sa.Column("evidence_strength", sa.String(20), nullable=False, server_default="STRONG"),
        sa.Column("resolution_status", sa.String(30), nullable=False, server_default="ACTIVE", index=True),
        sa.Column("correlation_method", sa.String(50), nullable=False, server_default="EXACT_IDENTIFIER"),
        sa.Column("correlation_version", sa.String(20), nullable=False, server_default="1.0.0"),
        sa.Column("first_observed", sa.DateTime(), nullable=False),
        sa.Column("last_observed", sa.DateTime(), nullable=False),
        sa.Column("source_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("is_manual", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("author_id", sa.String(64), nullable=True),
        sa.Column("staleness_reason", sa.Text(), nullable=True),
        sa.Column("conflicting_sources", sa.JSON(), nullable=False),
        sa.Column("metadata", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 6. relationship_evidence
    op.create_table(
        "relationship_evidence",
        sa.Column("evidence_binding_id", sa.String(64), primary_key=True),
        sa.Column("relationship_id", sa.String(64), sa.ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("evidence_id", sa.String(64), nullable=False, index=True),
        sa.Column("finding_id", sa.String(64), nullable=True, index=True),
        sa.Column("analysis_id", sa.String(64), nullable=False, index=True),
        sa.Column("evidence_strength", sa.String(20), nullable=False, server_default="DIRECT"),
        sa.Column("observation_summary", sa.Text(), nullable=False),
    )

    # 7. relationship_provenance
    op.create_table(
        "relationship_provenance",
        sa.Column("provenance_id", sa.String(64), primary_key=True),
        sa.Column("relationship_id", sa.String(64), sa.ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_system", sa.String(64), nullable=False),
        sa.Column("rule_id", sa.String(64), nullable=False),
        sa.Column("rule_version", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 8. correlation_candidates
    op.create_table(
        "correlation_candidates",
        sa.Column("candidate_id", sa.String(64), primary_key=True),
        sa.Column("source_entity_id", sa.String(64), nullable=False, index=True),
        sa.Column("target_entity_id", sa.String(64), nullable=False, index=True),
        sa.Column("relationship_type", sa.String(50), nullable=False),
        sa.Column("candidate_score", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="MEDIUM"),
        sa.Column("evidence_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("correlation_method", sa.String(50), nullable=False, server_default="NORMALIZED_IDENTIFIER"),
        sa.Column("false_correlation_penalty", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 9. intelligence_correlation_runs
    op.create_table(
        "intelligence_correlation_runs",
        sa.Column("run_id", sa.String(64), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("analysis_scope", sa.JSON(), nullable=False),
        sa.Column("correlation_version", sa.String(20), nullable=False, server_default="1.0.0"),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="RUNNING"),
        sa.Column("candidate_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("accepted_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("rejected_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("uncertain_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
    )

    # 10. threat_campaigns
    op.create_table(
        "threat_campaigns",
        sa.Column("campaign_id", sa.String(64), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("campaign_type", sa.String(50), nullable=False, server_default="PHISHING_CAMPAIGN", index=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH"),
        sa.Column("first_seen", sa.DateTime(), nullable=False),
        sa.Column("last_seen", sa.DateTime(), nullable=False),
        sa.Column("entity_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("analysis_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("finding_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("evidence_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("relationship_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("threat_actor", sa.String(128), nullable=False, server_default="UNKNOWN"),
        sa.Column("threat_actor_confidence", sa.String(50), nullable=False, server_default="UNCONFIRMED_ASSOCIATION"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 11. campaign_entities
    op.create_table(
        "campaign_entities",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("campaign_id", sa.String(64), sa.ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("entity_id", sa.String(64), sa.ForeignKey("intelligence_entities.entity_id", ondelete="CASCADE"), nullable=False, index=True),
    )

    # 12. campaign_relationships
    op.create_table(
        "campaign_relationships",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("campaign_id", sa.String(64), sa.ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("relationship_id", sa.String(64), sa.ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True),
    )

    # 13. attack_chains
    op.create_table(
        "attack_chains",
        sa.Column("chain_id", sa.String(64), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("campaign_id", sa.String(64), sa.ForeignKey("threat_campaigns.campaign_id", ondelete="SET NULL"), nullable=True, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("entry_point", sa.Text(), nullable=False),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH"),
        sa.Column("status", sa.String(20), nullable=False, server_default="ACTIVE"),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("finding_ids", sa.JSON(), nullable=False),
        sa.Column("missing_steps_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("uncertainty_summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # 14. attack_chain_steps
    op.create_table(
        "attack_chain_steps",
        sa.Column("step_id", sa.String(64), primary_key=True),
        sa.Column("chain_id", sa.String(64), sa.ForeignKey("attack_chains.chain_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("step_number", sa.Integer(), nullable=False),
        sa.Column("stage", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("step_state", sa.String(30), nullable=False, server_default="CONFIRMED_STEP"),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="HIGH"),
        sa.Column("entity_ids", sa.JSON(), nullable=False),
        sa.Column("evidence_ids", sa.JSON(), nullable=False),
        sa.Column("finding_ids", sa.JSON(), nullable=False),
        sa.Column("missing_evidence_note", sa.Text(), nullable=True),
    )

    # 15. threat_actor_associations
    op.create_table(
        "threat_actor_associations",
        sa.Column("association_id", sa.String(64), primary_key=True),
        sa.Column("actor_name", sa.String(128), nullable=False, index=True),
        sa.Column("campaign_id", sa.String(64), sa.ForeignKey("threat_campaigns.campaign_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("confidence", sa.String(20), nullable=False, server_default="LOW"),
        sa.Column("source", sa.String(64), nullable=False, server_default="THREAT_INTEL"),
        sa.Column("evidence", sa.Text(), nullable=False, server_default=""),
        sa.Column("attribution_type", sa.String(50), nullable=False, server_default="UNCONFIRMED_ASSOCIATION"),
        sa.Column("attribution_status", sa.String(30), nullable=False, server_default="UNCONFIRMED"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 16. graph_versions
    op.create_table(
        "graph_versions",
        sa.Column("graph_version_id", sa.String(64), primary_key=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("version_number", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("schema_version", sa.String(20), nullable=False, server_default="4.0.0"),
        sa.Column("correlation_version", sa.String(20), nullable=False, server_default="1.0.0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("created_by", sa.String(64), nullable=False, server_default="SYSTEM"),
        sa.Column("change_summary", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(64), nullable=False),
    )

    # 17. graph_snapshots
    op.create_table(
        "graph_snapshots",
        sa.Column("snapshot_id", sa.String(64), primary_key=True),
        sa.Column("graph_version_id", sa.String(64), sa.ForeignKey("graph_versions.graph_version_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("case_id", sa.String(64), nullable=True, index=True),
        sa.Column("snapshot_data", sa.JSON(), nullable=False),
        sa.Column("total_nodes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("total_edges", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("content_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 18. graph_changes
    op.create_table(
        "graph_changes",
        sa.Column("change_id", sa.String(64), primary_key=True),
        sa.Column("graph_version_id", sa.String(64), sa.ForeignKey("graph_versions.graph_version_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("change_type", sa.String(50), nullable=False),
        sa.Column("target_id", sa.String(64), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    # 19. correlation_review_queue
    op.create_table(
        "correlation_review_queue",
        sa.Column("review_id", sa.String(64), primary_key=True),
        sa.Column("relationship_id", sa.String(64), sa.ForeignKey("intelligence_relationships.relationship_id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("source_entity_value", sa.Text(), nullable=False),
        sa.Column("target_entity_value", sa.Text(), nullable=False),
        sa.Column("relationship_type", sa.String(50), nullable=False),
        sa.Column("confidence", sa.String(20), nullable=False),
        sa.Column("flag_reason", sa.String(50), nullable=False),
        sa.Column("priority", sa.String(20), nullable=False, server_default="MEDIUM"),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING", index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("correlation_review_queue")
    op.drop_table("graph_changes")
    op.drop_table("graph_snapshots")
    op.drop_table("graph_versions")
    op.drop_table("threat_actor_associations")
    op.drop_table("attack_chain_steps")
    op.drop_table("attack_chains")
    op.drop_table("campaign_relationships")
    op.drop_table("campaign_entities")
    op.drop_table("threat_campaigns")
    op.drop_table("intelligence_correlation_runs")
    op.drop_table("correlation_candidates")
    op.drop_table("relationship_provenance")
    op.drop_table("relationship_evidence")
    op.drop_table("intelligence_relationships")
    op.drop_table("entity_resolution_records")
    op.drop_table("entity_observations")
    op.drop_table("entity_aliases")
    op.drop_table("intelligence_entities")
