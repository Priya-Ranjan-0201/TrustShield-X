"""
TruthShield X — Knowledge Relationship Manager (Phase 19).

Manages knowledge graph edges across all 27 relationship types with explicit source provenance, evidence trail, and revocation tracking.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import (
    KnowledgeRelationshipDTO,
    KnowledgeRelationTypeLiteral,
)


class KnowledgeRelationshipManager:
    """Manages knowledge relationships with provenance, evidence linkage, and revocation tracking."""

    def __init__(self):
        self._relationships: Dict[str, KnowledgeRelationshipDTO] = {}
        self._initialize_seed_relationships()

    def _initialize_seed_relationships(self):
        seeds = [
            ("srv_checkout_production", "svc_payment_gateway", "HOSTS", ["ev_pcap_trace_88"], 0.98),
            ("svc_payment_gateway", "ctrl_waf_edge_01", "PROTECTS", ["ev_config_dump_01"], 0.95),
            ("svc_payment_gateway", "cve_2026_9942", "EXPOSES", ["ev_vuln_scan_44"], 0.90),
            ("cve_2026_9942", "camp_shadow_hydra", "INDICATES", ["ev_threat_intel_feed"], 0.85),
            ("usr_admin_svc", "srv_checkout_production", "ACCESSES", ["ev_audit_log_90"], 0.96),
        ]
        for src, tgt, rel_type, ev_list, conf in seeds:
            rel = KnowledgeRelationshipDTO(
                source_id=src,
                target_id=tgt,
                relation_type=rel_type,  # type: ignore
                evidence=ev_list,
                confidence=conf,
                method="AUTOMATED_DISCOVERY",
                actor="FABRIC_SEED_LOADER",
            )
            self._relationships[rel.relationship_id] = rel

    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relation_type: KnowledgeRelationTypeLiteral,
        evidence: Optional[List[str]] = None,
        confidence: float = 0.85,
        source: str = "DISCOVERY_ENGINE",
        method: str = "GRAPH_CORRELATION",
        actor: str = "SYSTEM_FABRIC",
    ) -> KnowledgeRelationshipDTO:
        """Creates a relationship with explicit evidence and provenance."""
        rel = KnowledgeRelationshipDTO(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            source=source,
            evidence=evidence or [],
            confidence=confidence,
            method=method,
            actor=actor,
        )
        self._relationships[rel.relationship_id] = rel
        return rel

    def revoke_relationship(self, relationship_id: str) -> Optional[KnowledgeRelationshipDTO]:
        """Revokes a relationship while keeping historical traceability."""
        rel = self._relationships.get(relationship_id)
        if not rel:
            return None

        revoked = KnowledgeRelationshipDTO(
            relationship_id=rel.relationship_id,
            source_id=rel.source_id,
            target_id=rel.target_id,
            relation_type=rel.relation_type,
            source=rel.source,
            evidence=rel.evidence,
            confidence=0.0,
            timestamp=rel.timestamp,
            method=rel.method,
            actor=rel.actor,
            version=rel.version + 1,
            is_revoked=True,
        )
        self._relationships[relationship_id] = revoked
        return revoked

    def get_relationships_for_node(self, node_id: str) -> List[KnowledgeRelationshipDTO]:
        """Returns all incoming and outgoing active relationships for an entity."""
        return [
            r for r in self._relationships.values()
            if (r.source_id == node_id or r.target_id == node_id) and not r.is_revoked
        ]

    def list_all(self, include_revoked: bool = False) -> List[KnowledgeRelationshipDTO]:
        """Lists all relationships."""
        if include_revoked:
            return list(self._relationships.values())
        return [r for r in self._relationships.values() if not r.is_revoked]
