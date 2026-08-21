"""
TruthShield X — Evidence Graph Engine (Phase 19).

Constructs and traverses the evidence graph linking observations, telemetry, intelligence, and conclusions.
"""

from typing import Dict, List, Set
from app.schemas.cyber_knowledge_fabric_models import (
    EvidenceGraphDTO,
    EvidenceGraphNodeDTO,
    EvidenceGraphEdgeDTO,
    EpistemicStatusLiteral,
)


class EvidenceGraphEngine:
    """Manages evidence nodes, relational linkages (SUPPORTS, CONTRADICTS, DERIVED_FROM), and graph traversal."""

    def __init__(self):
        self._nodes: Dict[str, EvidenceGraphNodeDTO] = {}
        self._edges: List[EvidenceGraphEdgeDTO] = []
        self._initialize_default_graph()

    def _initialize_default_graph(self):
        default_nodes = [
            ("ev_pcap_trace_88", "PCAP_TRACE", "PCAP Packet Stream 88", "EVIDENCE", 0.95),
            ("ev_audit_log_90", "AUDIT_LOG", "Kubernetes Audit Event 90", "EVIDENCE", 0.98),
            ("ev_vuln_scan_44", "VULN_SCAN", "Trivy Scan Finding 44", "OBSERVATION", 0.91),
            ("ev_threat_intel_feed", "INTEL_FEED", "MISP Shadow Hydra Feed", "EVIDENCE", 0.88),
            ("asrt_checkout_at_risk", "ASSERTION", "Checkout Service Vulnerable to Exploit", "INFERENCE", 0.89),
        ]
        for nid, ntype, lbl, epistemic, conf in default_nodes:
            self._nodes[nid] = EvidenceGraphNodeDTO(
                node_id=nid,
                node_type=ntype,
                label=lbl,
                epistemic_status=epistemic,  # type: ignore
                confidence=conf,
            )

        default_edges = [
            ("ev_pcap_trace_88", "asrt_checkout_at_risk", "SUPPORTS", 1.0),
            ("ev_vuln_scan_44", "asrt_checkout_at_risk", "SUPPORTS", 0.95),
            ("ev_threat_intel_feed", "asrt_checkout_at_risk", "SUPPORTS", 0.85),
        ]
        for src, tgt, rel, weight in default_edges:
            self._edges.append(EvidenceGraphEdgeDTO(
                source_id=src,
                target_id=tgt,
                relation=rel,  # type: ignore
                weight=weight,
            ))

    def add_node(
        self,
        node_id: str,
        node_type: str,
        label: str,
        epistemic_status: EpistemicStatusLiteral = "EVIDENCE",
        confidence: float = 0.90,
    ) -> EvidenceGraphNodeDTO:
        node = EvidenceGraphNodeDTO(
            node_id=node_id,
            node_type=node_type,
            label=label,
            epistemic_status=epistemic_status,
            confidence=confidence,
        )
        self._nodes[node_id] = node
        return node

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float = 1.0,
    ) -> EvidenceGraphEdgeDTO:
        edge = EvidenceGraphEdgeDTO(
            source_id=source_id,
            target_id=target_id,
            relation=relation,  # type: ignore
            weight=weight,
        )
        self._edges.append(edge)
        return edge

    def get_supporting_evidence(self, target_id: str) -> List[EvidenceGraphNodeDTO]:
        """Returns all evidence nodes with SUPPORTS relation to target."""
        supp_ids = [e.source_id for e in self._edges if e.target_id == target_id and e.relation == "SUPPORTS"]
        return [self._nodes[nid] for nid in supp_ids if nid in self._nodes]

    def get_contradicting_evidence(self, target_id: str) -> List[EvidenceGraphNodeDTO]:
        """Returns all evidence nodes with CONTRADICTS relation to target."""
        contra_ids = [e.source_id for e in self._edges if e.target_id == target_id and e.relation == "CONTRADICTS"]
        return [self._nodes[nid] for nid in contra_ids if nid in self._nodes]

    def build_graph(self) -> EvidenceGraphDTO:
        """Constructs aggregated graph representation."""
        contra_count = len([e for e in self._edges if e.relation == "CONTRADICTS"])
        return EvidenceGraphDTO(
            nodes=list(self._nodes.values()),
            edges=self._edges,
            total_evidence_nodes=len(self._nodes),
            contradiction_count=contra_count,
        )
