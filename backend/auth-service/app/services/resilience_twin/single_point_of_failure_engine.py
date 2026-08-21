"""
TruthShield X — Single Point of Failure (SPOF) & Cascading Failure Engine (Phase 18).

Detects critical concentration risks and models downstream cascading service degradation.
"""

from typing import List, Dict, Any
from app.schemas.cyber_resilience_twin_models import SinglePointOfFailureDTO
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine


class SinglePointOfFailureEngine:
    """Analyzes dependency topologies to identify single points of failure."""

    def __init__(self, dep_engine: CyberDependencyGraphEngine):
        self.dep_engine = dep_engine

    def identify_spofs(self) -> List[SinglePointOfFailureDTO]:
        """Identifies resources whose failure would cascade into multiple services."""
        graph = self.dep_engine.build_graph()
        spofs: List[SinglePointOfFailureDTO] = []

        # Count incoming dependency bottlenecks
        target_counts: Dict[str, List[str]] = {}
        for edge in graph.edges:
            target_counts.setdefault(edge.target_id, []).append(edge.source_id)

        for target_id, dependents in target_counts.items():
            if len(dependents) >= 2:  # 2 or more services depend on this single resource
                severity = "CRITICAL" if len(dependents) >= 3 else "HIGH"
                spof = SinglePointOfFailureDTO(
                    resource_id=target_id,
                    resource_type="SHARED_SERVICE",
                    impact_severity=severity,
                    cascading_affected_services=dependents,
                    is_spof=True,
                    mitigation_suggestion=f"Deploy redundant multi-zone replica for '{target_id}' to eliminate single point of failure.",
                )
                spofs.append(spof)

        return spofs

    def model_cascading_failure(self, failed_resource_id: str) -> Dict[str, Any]:
        """Simulates cascading failure path from a single node breakdown."""
        deps = self.dep_engine.get_dependencies_for_resource(failed_resource_id)
        downstream = [d.source_id for d in deps if d.target_id == failed_resource_id]

        return {
            "initial_failed_node": failed_resource_id,
            "cascade_depth": 1 if downstream else 0,
            "affected_service_count": len(downstream),
            "affected_services": downstream,
            "business_impact_level": "SEVERE" if len(downstream) >= 2 else "MODERATE",
            "is_simulated": True,
        }
