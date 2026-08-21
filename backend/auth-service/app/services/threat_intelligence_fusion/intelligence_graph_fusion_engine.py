"""
TruthShield X — Intelligence Graph Fusion & Temporal Provenance Engine (Phase 33).

Maintains a graph of actors, campaigns, indicators, malware, vulnerabilities,
and techniques with temporal edges, provenance tracking, and immutable snapshots.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import hashlib
import json

from app.schemas.threat_intelligence_fusion_models import IntelligenceSnapshotDTO


class IntelligenceGraphFusionEngine:
    """Temporal cyber threat intelligence knowledge graph."""

    def __init__(self):
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[Dict[str, Any]] = []
        self._snapshots: Dict[str, IntelligenceSnapshotDTO] = {}
        self._seed_default_graph()

    def _seed_default_graph(self):
        # Nodes
        self.add_node("act_apt_ember_bear", "ACTOR", {"name": "Ember Bear (APT-88)"})
        self.add_node("cmp_darkstorm_apac", "CAMPAIGN", {"name": "Operation DarkStorm APAC"})
        self.add_node("ind_c2_darkstorm", "INDICATOR", {"value": "http://malicious-c2.darkstorm-threat.com/beacon"})
        self.add_node("mal_cobalt_beacon", "MALWARE", {"family": "Cobalt Strike Beacon"})
        self.add_node("T1071.001", "TECHNIQUE", {"name": "Web Protocols: HTTP/HTTPS"})
        self.add_node("ast_payment_gw_01", "ASSET", {"name": "APAC Core Payment Gateway"})

        # Edges
        self.add_edge("act_apt_ember_bear", "OPERATES", "cmp_darkstorm_apac", "ev_cert_in_advisory_492")
        self.add_edge("cmp_darkstorm_apac", "USES", "mal_cobalt_beacon", "ev_telemetry_flow_20260714")
        self.add_edge("mal_cobalt_beacon", "ASSOCIATED_WITH", "ind_c2_darkstorm", "ev_sandbox_detonation")
        self.add_edge("mal_cobalt_beacon", "USES", "T1071.001", "ev_attck_mapping")
        self.add_edge("cmp_darkstorm_apac", "TARGETS", "ast_payment_gw_01", "ev_asset_correlation")

    def add_node(self, node_id: str, node_type: str, properties: Dict[str, Any]) -> Dict[str, Any]:
        node = {
            "node_id": node_id,
            "node_type": node_type,
            "properties": properties,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._nodes[node_id] = node
        return node

    def add_edge(
        self,
        source_node_id: str,
        relationship: str,
        target_node_id: str,
        provenance_evidence: str,
        first_seen: Optional[str] = None,
        last_seen: Optional[str] = None,
    ) -> Dict[str, Any]:
        edge = {
            "source": source_node_id,
            "relationship": relationship,
            "target": target_node_id,
            "provenance": provenance_evidence,
            "first_seen": first_seen or datetime.now(timezone.utc).isoformat(),
            "last_seen": last_seen or datetime.now(timezone.utc).isoformat(),
            "confidence": 0.90,
        }
        self._edges.append(edge)
        return edge

    def query_graph(self, entity_id: Optional[str] = None) -> Dict[str, Any]:
        if not entity_id:
            return {"nodes": list(self._nodes.values()), "edges": self._edges}

        # Filter subgraph
        related_edges = [e for e in self._edges if e["source"] == entity_id or e["target"] == entity_id]
        related_node_ids = {entity_id}
        for e in related_edges:
            related_node_ids.add(e["source"])
            related_node_ids.add(e["target"])

        related_nodes = [self._nodes[nid] for nid in related_node_ids if nid in self._nodes]
        return {"nodes": related_nodes, "edges": related_edges}

    def create_snapshot(self, snapshot_type: str, entity_id: str) -> IntelligenceSnapshotDTO:
        subgraph = self.query_graph(entity_id)
        content_str = json.dumps(subgraph, sort_keys=True)
        snap_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        snap_id = f"snap_{snap_hash[:12]}"

        dto = IntelligenceSnapshotDTO(
            snapshot_id=snap_id,
            snapshot_type=snapshot_type,
            entity_id=entity_id,
            content_state=subgraph,
            snapshot_hash=snap_hash,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        self._snapshots[snap_id] = dto
        return dto

    def list_snapshots(self) -> List[IntelligenceSnapshotDTO]:
        return list(self._snapshots.values())
