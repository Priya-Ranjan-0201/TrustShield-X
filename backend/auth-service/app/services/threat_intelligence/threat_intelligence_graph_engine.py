"""
TruthShield X — Threat Intelligence Graph Engine (Phase 22).

Constructs and queries the Cyber Threat Intelligence Graph connecting indicators, malware, techniques, campaigns, and assets.
"""

from typing import Dict, List, Optional, Set
from collections import deque
from app.schemas.threat_intelligence_fabric_models import (
    ThreatGraphNodeDTO,
    ThreatGraphEdgeDTO,
    ThreatIntelligenceGraphDTO,
    ThreatGraphEdgeTypeLiteral,
)


class ThreatIntelligenceGraphEngine:
    """Manages the in-memory Threat Intelligence Graph with bounded graph traversal analytics."""

    def __init__(self):
        self._nodes: Dict[str, ThreatGraphNodeDTO] = {}
        self._edges: List[ThreatGraphEdgeDTO] = []
        self._adj: Dict[str, List[ThreatGraphEdgeDTO]] = {}
        self._seed_default_graph()

    def _seed_default_graph(self):
        n1 = ThreatGraphNodeDTO(node_id="node_ind_c2", node_type="INDICATOR", label="c2.shadowhydra.net")
        n2 = ThreatGraphNodeDTO(node_id="node_infra_ip", node_type="INFRASTRUCTURE", label="198.51.100.42")
        n3 = ThreatGraphNodeDTO(node_id="node_malware_hydra", node_type="MALWARE", label="HydraLoader.v2")
        n4 = ThreatGraphNodeDTO(node_id="node_camp_shadow", node_type="CAMPAIGN", label="Operation ShadowStrike")
        n5 = ThreatGraphNodeDTO(node_id="node_tech_t1059", node_type="TECHNIQUE", label="T1059.001 (PowerShell)")
        n6 = ThreatGraphNodeDTO(node_id="node_asset_checkout", node_type="ASSET", label="srv_checkout_production")

        for n in [n1, n2, n3, n4, n5, n6]:
            self.add_node(n)

        self.add_edge(ThreatGraphEdgeDTO(source_node_id="node_ind_c2", target_node_id="node_infra_ip", relationship_type="RESOLVES_TO"))
        self.add_edge(ThreatGraphEdgeDTO(source_node_id="node_malware_hydra", target_node_id="node_ind_c2", relationship_type="USES"))
        self.add_edge(ThreatGraphEdgeDTO(source_node_id="node_malware_hydra", target_node_id="node_camp_shadow", relationship_type="PART_OF"))
        self.add_edge(ThreatGraphEdgeDTO(source_node_id="node_camp_shadow", target_node_id="node_tech_t1059", relationship_type="USES"))
        self.add_edge(ThreatGraphEdgeDTO(source_node_id="node_camp_shadow", target_node_id="node_asset_checkout", relationship_type="TARGETS"))

    def add_node(self, node: ThreatGraphNodeDTO) -> ThreatGraphNodeDTO:
        self._nodes[node.node_id] = node
        if node.node_id not in self._adj:
            self._adj[node.node_id] = []
        return node

    def add_edge(self, edge: ThreatGraphEdgeDTO) -> ThreatGraphEdgeDTO:
        self._edges.append(edge)
        if edge.source_node_id not in self._adj:
            self._adj[edge.source_node_id] = []
        self._adj[edge.source_node_id].append(edge)
        return edge

    def get_subgraph(self, start_node_id: str, max_depth: int = 3) -> ThreatIntelligenceGraphDTO:
        visited: Set[str] = set()
        queue = deque([(start_node_id, 0)])
        result_nodes: List[ThreatGraphNodeDTO] = []
        result_edges: List[ThreatGraphEdgeDTO] = []

        while queue:
            curr, depth = queue.popleft()
            if curr in visited or depth > max_depth:
                continue
            visited.add(curr)

            if curr in self._nodes:
                result_nodes.append(self._nodes[curr])

            for edge in self._adj.get(curr, []):
                result_edges.append(edge)
                if edge.target_node_id not in visited:
                    queue.append((edge.target_node_id, depth + 1))

        return ThreatIntelligenceGraphDTO(
            nodes=result_nodes,
            edges=result_edges,
            max_depth_limit=max_depth,
        )

    def shortest_path(self, start_node_id: str, end_node_id: str, max_depth: int = 5) -> List[str]:
        """Finds shortest path node IDs between two threat nodes."""
        if start_node_id not in self._nodes or end_node_id not in self._nodes:
            return []

        queue = deque([(start_node_id, [start_node_id])])
        visited = {start_node_id}

        while queue:
            curr, path = queue.popleft()
            if curr == end_node_id:
                return path
            if len(path) > max_depth:
                continue

            for edge in self._adj.get(curr, []):
                nxt = edge.target_node_id
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append((nxt, path + [nxt]))

        return []
