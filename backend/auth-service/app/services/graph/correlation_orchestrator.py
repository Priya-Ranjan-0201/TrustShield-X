"""Correlation Orchestrator (Phase 4.0 Part 5 — Sections 50, 85, 86, 100).

Master pipeline orchestrator that extracts, normalizes, deduplicates, resolves,
scores, and constructs the deterministic Unified Trust Intelligence Graph.
"""

import hashlib
import json
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.intelligence_graph_models import (
    CanonicalEntityDTO,
    GraphRelationshipDTO,
    CorrelationCandidateDTO,
    ThreatCampaignDTO,
    AttackChainDTO,
    UnifiedGraphResponseDTO,
    GraphSnapshotDTO,
    GraphVersionDTO,
    CorrelationRunDTO,
)
from app.services.graph.entity_normalizer import EntityNormalizer
from app.services.graph.entity_deduplication import EntityDeduplicationEngine
from app.services.graph.correlation_scoring_engine import CorrelationScoringEngine
from app.services.graph.campaign_correlation_engine import CampaignCorrelationEngine
from app.services.graph.attack_chain_engine import AttackChainEngine


class CorrelationOrchestrator:
    """Master orchestrator executing the deterministic correlation pipeline."""

    VERSION = "1.0.0"

    def run_pipeline(
        self,
        reports: List[ReportDocumentDTO],
        case_id: Optional[str] = None,
        organization_id: Optional[str] = None,
    ) -> Tuple[UnifiedGraphResponseDTO, GraphSnapshotDTO, CorrelationRunDTO]:
        started_at = datetime.now(timezone.utc).isoformat()
        raw_entities: List[CanonicalEntityDTO] = []

        # 1. Entity Extraction from Reports
        for doc in reports:
            raw_entities.extend(self._extract_entities_from_report(doc, organization_id))

        # 2. Normalization & Deduplication (Sections 4 & 41)
        entities = EntityDeduplicationEngine.deduplicate_entities(raw_entities)

        # 3. Candidate Generation & Correlation Scoring (Sections 11 & 53)
        relationships: List[GraphRelationshipDTO] = []
        candidate_count = 0
        accepted_count = 0
        rejected_count = 0

        for i in range(len(entities)):
            for j in range(i + 1, len(entities)):
                ent_a = entities[i]
                ent_b = entities[j]
                cand = CorrelationScoringEngine.evaluate_candidate(ent_a, ent_b)
                if cand:
                    candidate_count += 1
                    if cand.candidate_score >= 0.30:  # Accepted candidate
                        accepted_count += 1
                        rel_id = f"rel_{ent_a.entity_id}_{ent_b.entity_id}_{cand.relationship_type.lower()}"
                        relationships.append(
                            GraphRelationshipDTO(
                                relationship_id=rel_id,
                                source_entity_id=cand.source_entity_id,
                                target_entity_id=cand.target_entity_id,
                                relationship_type=cand.relationship_type,
                                confidence=cand.confidence,
                                evidence_strength="STRONG" if cand.candidate_score >= 0.7 else "MODERATE",
                                resolution_status="ACTIVE",
                                correlation_method=cand.correlation_method,
                                correlation_version=self.VERSION,
                                source_count=cand.evidence_count,
                            )
                        )
                    else:
                        rejected_count += 1

        # 4. Campaign Detection (Section 24)
        campaigns = CampaignCorrelationEngine.detect_campaigns(entities, relationships)

        # 5. Attack Chain Reconstruction (Section 28)
        attack_chains = AttackChainEngine.reconstruct_chains(entities, relationships, case_id=case_id)

        # 6. Deterministic Graph Hashing (Sections 43-44, 100)
        content_repr = json.dumps(
            {
                "entities": sorted([e.normalized_value for e in entities]),
                "relationships": sorted([f"{r.source_entity_id}->{r.target_entity_id}:{r.relationship_type}" for r in relationships]),
                "campaigns": sorted([c.campaign_id for c in campaigns]),
                "attack_chains": sorted([a.chain_id for a in attack_chains]),
            },
            sort_keys=True,
        )
        content_hash = hashlib.sha256(content_repr.encode("utf-8")).hexdigest()

        # 7. Unified Graph Response
        graph_response = UnifiedGraphResponseDTO(
            graph_version=1,
            total_nodes=len(entities),
            total_edges=len(relationships),
            nodes=entities,
            edges=relationships,
            campaigns=campaigns,
            attack_chains=attack_chains,
            truncated=False,
            query_timestamp=datetime.now(timezone.utc).isoformat(),
        )

        # 8. Graph Snapshot DTO
        snapshot = GraphSnapshotDTO(
            snapshot_id=f"snap_{content_hash[:16]}",
            graph_version_id="gver_001",
            case_id=case_id,
            nodes=entities,
            edges=relationships,
            campaigns=campaigns,
            attack_chains=attack_chains,
            total_nodes=len(entities),
            total_edges=len(relationships),
            content_hash=content_hash,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        # 9. Correlation Run Telemetry
        run_dto = CorrelationRunDTO(
            run_id=f"crun_{content_hash[:12]}",
            case_id=case_id,
            analysis_scope=[d.analysis_id for d in reports],
            correlation_version=self.VERSION,
            started_at=started_at,
            completed_at=datetime.now(timezone.utc).isoformat(),
            status="COMPLETED",
            candidate_count=candidate_count,
            accepted_count=accepted_count,
            rejected_count=rejected_count,
            uncertain_count=0,
            error_count=0,
        )

        return graph_response, snapshot, run_dto

    def _extract_entities_from_report(
        self, doc: ReportDocumentDTO, organization_id: Optional[str]
    ) -> List[CanonicalEntityDTO]:
        extracted: List[CanonicalEntityDTO] = []
        gen_time = doc.generated_at or datetime.now(timezone.utc).isoformat()

        # Extract Findings as entities
        for f in doc.major_findings:
            f_norm, f_disp, f_hash = EntityNormalizer.normalize("FINDING", f.finding_id)
            extracted.append(
                CanonicalEntityDTO(
                    entity_id=f"ent_f_{f.finding_id}",
                    entity_type="FINDING",
                    canonical_value=f.title,
                    display_value=f.title,
                    normalized_value=f_norm,
                    value_hash=f_hash,
                    confidence=f.confidence,
                    organization_id=organization_id,
                    first_seen=gen_time,
                    last_seen=gen_time,
                )
            )

        # Extract Evidence as entities
        for ev in doc.evidence_cards:
            ev_norm, ev_disp, ev_hash = EntityNormalizer.normalize("EVIDENCE", ev.card_id)
            extracted.append(
                CanonicalEntityDTO(
                    entity_id=f"ent_ev_{ev.card_id}",
                    entity_type="EVIDENCE",
                    canonical_value=ev.title,
                    display_value=ev.title,
                    normalized_value=ev_norm,
                    value_hash=ev_hash,
                    confidence=ev.confidence,
                    organization_id=organization_id,
                    first_seen=gen_time,
                    last_seen=gen_time,
                )
            )

        # Extract Threat Intelligence IOCs
        if doc.threat_intelligence and doc.threat_intelligence.observed_indicators:
            for ioc in doc.threat_intelligence.observed_indicators:
                norm, disp, v_hash = EntityNormalizer.normalize(ioc.indicator_type, ioc.indicator_value)
                extracted.append(
                    CanonicalEntityDTO(
                        entity_id=f"ent_ioc_{v_hash[:12]}",
                        entity_type="IOC",
                        canonical_value=norm,
                        display_value=disp,
                        normalized_value=norm,
                        value_hash=v_hash,
                        confidence=ioc.confidence,
                        organization_id=organization_id,
                        first_seen=gen_time,
                        last_seen=gen_time,
                    )
                )

        return extracted
