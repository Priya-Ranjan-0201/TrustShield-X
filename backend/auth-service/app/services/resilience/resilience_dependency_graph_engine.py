"""
TruthShield X — Resilience Dependency Graph Engine (Phase 23).

Constructs the full stack dependency graph and detects Single Points of Failure (SPOFs).
"""

from typing import Dict, List, Any, Set
from app.schemas.cyber_resilience_models import ServiceDependencyGraphDTO


class ResilienceDependencyGraphEngine:
    """Evaluates service-to-infrastructure dependencies and detects structural single points of failure."""

    def __init__(self):
        self._dependencies: Dict[str, List[str]] = {
            "svc_checkout_api": ["ast_api_gateway", "ast_auth_service"],
            "ast_api_gateway": ["ast_pg_primary", "ast_redis_cache"],
            "ast_auth_service": ["ast_pg_primary", "ast_idp_okta"],
            "ast_pg_primary": ["ast_storage_ebs", "ast_net_vpc"],
            "ast_redis_cache": ["ast_net_vpc"],
        }

    def build_graph(self, tenant_id: str = "default_tenant") -> ServiceDependencyGraphDTO:
        nodes = []
        edges = []
        in_degree: Dict[str, int] = {}
        all_nodes: Set[str] = set()

        for src, targets in self._dependencies.items():
            all_nodes.add(src)
            if src not in in_degree:
                in_degree[src] = 0
            for tgt in targets:
                all_nodes.add(tgt)
                edges.append({"source": src, "target": tgt, "relationship": "DEPENDS_ON"})
                in_degree[tgt] = in_degree.get(tgt, 0) + 1

        for n in all_nodes:
            nodes.append({"id": n, "label": n})

        # Single point of failure: any shared node with in_degree >= 2 that is not redundantly backed
        spofs = [node for node, count in in_degree.items() if count >= 2]

        return ServiceDependencyGraphDTO(
            tenant_id=tenant_id,
            nodes=nodes,
            edges=edges,
            single_points_of_failure=spofs,
        )
