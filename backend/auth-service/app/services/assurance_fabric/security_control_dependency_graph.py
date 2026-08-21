"""
TruthShield X — Security Control Dependency Graph Engine (Phase 24).

Maps software components, policies, and pipelines to security controls to calculate change impact.
"""

from typing import Dict, List, Set, Any


class SecurityControlDependencyGraph:
    """Computes dependency relationships between operational components and security controls."""

    def __init__(self):
        self._component_to_controls: Dict[str, List[str]] = {
            "app_auth_service": ["ctl_tenant_isolation", "ctl_four_eyes_response"],
            "db_postgres_cluster": ["ctl_tenant_isolation", "ctl_immutable_audit"],
            "api_gateway": ["ctl_four_eyes_response"],
            "threat_intel_feed": ["ctl_tenant_isolation"],
        }

    def get_affected_controls(self, changed_components: List[str]) -> List[str]:
        affected: Set[str] = set()
        for comp in changed_components:
            if comp in self._component_to_controls:
                affected.update(self._component_to_controls[comp])
        return sorted(list(affected))

    def build_graph(self) -> Dict[str, Any]:
        nodes = []
        edges = []
        for comp, controls in self._component_to_controls.items():
            nodes.append({"id": comp, "type": "COMPONENT"})
            for ctl in controls:
                nodes.append({"id": ctl, "type": "CONTROL"})
                edges.append({"source": comp, "target": ctl, "relationship": "GOVERNS"})

        # Deduplicate nodes by id
        unique_nodes = {n["id"]: n for n in nodes}.values()
        return {"nodes": list(unique_nodes), "edges": edges}
