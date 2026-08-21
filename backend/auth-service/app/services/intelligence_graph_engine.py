"""Master Unified Trust Intelligence Graph Engine (Phase 4.0 Part 5 — Section 1).

Master facade coordinating entity extraction, normalization, resolution, deduplication,
correlation scoring, campaign clustering, attack-chain reconstruction, and graph queries.
"""

from typing import List, Dict, Any, Optional, Tuple
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    ThreatCampaignDTO,
    AttackChainDTO,
    UnifiedGraphResponseDTO,
    GraphSnapshotDTO,
    GraphDiffDTO,
    CorrelationRunDTO,
    CorrelationExplanationDTO,
)
from app.services.graph.entity_normalizer import EntityNormalizer
from app.services.graph.entity_resolution_engine import EntityResolutionEngine
from app.services.graph.entity_deduplication import EntityDeduplicationEngine
from app.services.graph.correlation_scoring_engine import CorrelationScoringEngine
from app.services.graph.correlation_explanation_engine import CorrelationExplanationEngine
from app.services.graph.campaign_correlation_engine import CampaignCorrelationEngine
from app.services.graph.attack_chain_engine import AttackChainEngine
from app.services.graph.correlation_orchestrator import CorrelationOrchestrator


class IntelligenceGraphEngine:
    """Master facade for the Unified Trust Intelligence Graph."""

    VERSION = "1.0.0"

    def __init__(self):
        self.orchestrator = CorrelationOrchestrator()

    def build_intelligence_graph(
        self,
        reports: List[ReportDocumentDTO],
        case_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Tuple[UnifiedGraphResponseDTO, GraphSnapshotDTO, CorrelationRunDTO]:
        """Executes full pipeline and constructs authoritative intelligence graph."""
        return self.orchestrator.run_pipeline(reports, case_id=case_id, organization_id=organization_id)

    def explain_relationship(
        self,
        relationship: GraphRelationshipDTO,
        source_ent: Optional[CanonicalEntityDTO] = None,
        target_ent: Optional[CanonicalEntityDTO] = None,
    ) -> CorrelationExplanationDTO:
        """Returns structured explanation of a graph relationship."""
        return CorrelationExplanationEngine.explain(relationship, source_ent, target_ent)

    def compare_snapshots(
        self, base_snapshot: GraphSnapshotDTO, target_snapshot: GraphSnapshotDTO
    ) -> GraphDiffDTO:
        """Computes structural diff between two historical graph snapshots."""
        base_node_ids = {n.entity_id for n in base_snapshot.nodes}
        target_node_ids = {n.entity_id for n in target_snapshot.nodes}

        base_rel_ids = {r.relationship_id for r in base_snapshot.edges}
        target_rel_ids = {r.relationship_id for r in target_snapshot.edges}

        added_nodes = list(target_node_ids - base_node_ids)
        removed_nodes = list(base_node_ids - target_node_ids)

        added_rels = list(target_rel_ids - base_rel_ids)
        removed_rels = list(base_rel_ids - target_rel_ids)

        # Track confidence changes
        base_rel_map = {r.relationship_id: r.confidence for r in base_snapshot.edges}
        target_rel_map = {r.relationship_id: r.confidence for r in target_snapshot.edges}
        changed_conf = {}
        for r_id in target_rel_ids.intersection(base_rel_ids):
            if base_rel_map[r_id] != target_rel_map[r_id]:
                changed_conf[r_id] = f"{base_rel_map[r_id]} -> {target_rel_map[r_id]}"

        return GraphDiffDTO(
            base_version=1,
            target_version=2,
            added_entity_ids=added_nodes,
            removed_entity_ids=removed_nodes,
            added_relationship_ids=added_rels,
            removed_relationship_ids=removed_rels,
            changed_confidence_relationships=changed_conf,
        )
