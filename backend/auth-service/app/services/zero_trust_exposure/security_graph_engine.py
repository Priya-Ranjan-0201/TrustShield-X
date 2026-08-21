"""
TruthShield X — Security Graph & Temporality Engine (Phase 34)
=============================================================
Unified Knowledge & Security Graph modeling:
- Nodes: IDENTITY, DEVICE, SESSION, ASSET, SERVICE, NETWORK, VULNERABILITY, CREDENTIAL, CONTROL, RESOURCE, TENANT.
- Edges: AUTHENTICATES, ACCESSES, CONNECTS_TO, DEPENDS_ON, EXPOSES, PROTECTS, REACHES, TRUSTS, AUTHORIZED_FOR.
- Temporality: valid_from, valid_until, first_seen, last_seen.
- Provenance & Multi-Tenant Isolation with Historical Reconstruction.
"""

from typing import Dict, Any, List, Optional, Set
import datetime
import uuid


class SecurityGraphEngine:
    NODE_TYPES = {
        "IDENTITY", "DEVICE", "SESSION", "ASSET", "SERVICE",
        "NETWORK", "VULNERABILITY", "CREDENTIAL", "CONTROL", "RESOURCE", "TENANT"
    }

    EDGE_TYPES = {
        "AUTHENTICATES", "ACCESSES", "CONNECTS_TO", "DEPENDS_ON",
        "EXPOSES", "PROTECTS", "REACHES", "TRUSTS", "AUTHORIZED_FOR"
    }

    def __init__(self):
        # tenant_id -> node_id -> node_data
        self._nodes: Dict[str, Dict[str, Dict[str, Any]]] = {}
        # tenant_id -> edge_id -> edge_data
        self._edges: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def add_node(
        self,
        tenant_id: str,
        node_id: str,
        node_type: str,
        properties: Optional[Dict[str, Any]] = None,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None
    ) -> Dict[str, Any]:
        if node_type not in self.NODE_TYPES:
            raise ValueError(f"Invalid node_type: {node_type}. Must be one of {self.NODE_TYPES}")

        if tenant_id not in self._nodes:
            self._nodes[tenant_id] = {}

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        node = {
            "node_id": node_id,
            "tenant_id": tenant_id,
            "node_type": node_type,
            "properties": properties or {},
            "first_seen": now,
            "last_seen": now,
            "valid_from": valid_from or now,
            "valid_until": valid_until,
            "is_active": True
        }
        self._nodes[tenant_id][node_id] = node
        return node

    def add_edge(
        self,
        tenant_id: str,
        edge_id: str,
        source_node_id: str,
        target_node_id: str,
        edge_type: str,
        confidence: float = 1.0,
        evidence: Optional[Dict[str, Any]] = None,
        valid_from: Optional[str] = None,
        valid_until: Optional[str] = None
    ) -> Dict[str, Any]:
        if edge_type not in self.EDGE_TYPES:
            raise ValueError(f"Invalid edge_type: {edge_type}. Must be one of {self.EDGE_TYPES}")

        # Ensure tenant isolation and node existence
        tenant_nodes = self._nodes.get(tenant_id, {})
        if source_node_id not in tenant_nodes or target_node_id not in tenant_nodes:
            raise ValueError("Both source and target nodes must exist in the same tenant context before connecting an edge")

        if tenant_id not in self._edges:
            self._edges[tenant_id] = {}

        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        edge = {
            "edge_id": edge_id,
            "tenant_id": tenant_id,
            "source_node_id": source_node_id,
            "target_node_id": target_node_id,
            "edge_type": edge_type,
            "confidence": min(1.0, max(0.0, confidence)),
            "evidence": evidence or {},
            "first_seen": now,
            "last_seen": now,
            "valid_from": valid_from or now,
            "valid_until": valid_until,
            "is_active": True
        }
        self._edges[tenant_id][edge_id] = edge
        return edge

    def get_nodes(self, tenant_id: str, node_type: Optional[str] = None) -> List[Dict[str, Any]]:
        tenant_nodes = self._nodes.get(tenant_id, {})
        if node_type:
            return [n for n in tenant_nodes.values() if n["node_type"] == node_type]
        return list(tenant_nodes.values())

    def get_edges(self, tenant_id: str, edge_type: Optional[str] = None) -> List[Dict[str, Any]]:
        tenant_edges = self._edges.get(tenant_id, {})
        if edge_type:
            return [e for e in tenant_edges.values() if e["edge_type"] == edge_type]
        return list(tenant_edges.values())

    def query_graph_at_time(self, tenant_id: str, timestamp: str) -> Dict[str, Any]:
        """Historical graph reconstruction at a given point in time."""
        tenant_nodes = self._nodes.get(tenant_id, {})
        tenant_edges = self._edges.get(tenant_id, {})

        valid_nodes = []
        for n in tenant_nodes.values():
            if n["valid_from"] <= timestamp:
                if not n.get("valid_until") or n["valid_until"] >= timestamp:
                    valid_nodes.append(n)

        valid_edges = []
        for e in tenant_edges.values():
            if e["valid_from"] <= timestamp:
                if not e.get("valid_until") or e["valid_until"] >= timestamp:
                    valid_edges.append(e)

        return {
            "tenant_id": tenant_id,
            "query_timestamp": timestamp,
            "nodes_count": len(valid_nodes),
            "edges_count": len(valid_edges),
            "nodes": valid_nodes,
            "edges": valid_edges
        }

    def find_paths(
        self,
        tenant_id: str,
        start_node_id: str,
        end_node_id: str,
        max_depth: int = 5
    ) -> List[List[Dict[str, Any]]]:
        """Finds all paths from start_node_id to end_node_id respecting graph direction."""
        tenant_edges = self._edges.get(tenant_id, {})
        if not tenant_edges:
            return []

        adj: Dict[str, List[Dict[str, Any]]] = {}
        for edge in tenant_edges.values():
            src = edge["source_node_id"]
            if src not in adj:
                adj[src] = []
            adj[src].append(edge)

        paths = []

        def dfs(current: str, target: str, current_path: List[Dict[str, Any]], visited: Set[str], depth: int):
            if depth > max_depth:
                return
            if current == target:
                paths.append(list(current_path))
                return

            visited.add(current)
            for edge in adj.get(current, []):
                nxt = edge["target_node_id"]
                if nxt not in visited:
                    current_path.append(edge)
                    dfs(nxt, target, current_path, visited, depth + 1)
                    current_path.pop()
            visited.remove(current)

        dfs(start_node_id, end_node_id, [], set(), 0)
        return paths


security_graph_engine = SecurityGraphEngine()
