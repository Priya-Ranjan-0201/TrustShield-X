"""
TruthShield X — Cyber Dependency Graph Engine (Phase 18).

Builds and traverses topological dependency graphs with explicit confidence states (VERIFIED, OBSERVED, INFERRED, UNKNOWN).
"""

from typing import Dict, List, Optional, Any
from app.schemas.cyber_resilience_twin_models import (
    CyberDependencyDTO,
    CyberDependencyGraphDTO,
    DependencyRelationLiteral,
    DependencyConfidenceStateLiteral,
)


class CyberDependencyGraphEngine:
    """Manages system dependencies, service linkages, and confidence ratings."""

    def __init__(self):
        self._dependencies: List[CyberDependencyDTO] = []
        self._initialize_default_graph()

    def _initialize_default_graph(self):
        defaults = [
            CyberDependencyDTO(
                source_id="service_api_gateway",
                target_id="service_auth_jwt",
                relation_type="SERVICE_DEPENDS_ON",
                confidence_state="VERIFIED",
                confidence_score=0.98,
            ),
            CyberDependencyDTO(
                source_id="service_billing",
                target_id="service_auth_jwt",
                relation_type="SERVICE_DEPENDS_ON",
                confidence_state="VERIFIED",
                confidence_score=0.95,
            ),
            CyberDependencyDTO(
                source_id="service_auth_jwt",
                target_id="db_primary_users",
                relation_type="DATA_STORED_ON",
                confidence_state="VERIFIED",
                confidence_score=0.95,
            ),
            CyberDependencyDTO(
                source_id="control_waf_edge",
                target_id="service_api_gateway",
                relation_type="CONTROL_PROTECTS",
                confidence_state="VERIFIED",
                confidence_score=0.99,
            ),
            CyberDependencyDTO(
                source_id="service_billing",
                target_id="service_payment_vault",
                relation_type="SERVICE_DEPENDS_ON",
                confidence_state="OBSERVED",
                confidence_score=0.85,
            ),
        ]
        self._dependencies.extend(defaults)

    def add_dependency(
        self,
        source_id: str,
        target_id: str,
        relation_type: DependencyRelationLiteral,
        confidence_state: DependencyConfidenceStateLiteral = "VERIFIED",
        confidence_score: float = 0.95,
        source: str = "OBSERVED_TELEMETRY",
    ) -> CyberDependencyDTO:
        """Adds a verified or inferred dependency relation."""
        dep = CyberDependencyDTO(
            source_id=source_id,
            target_id=target_id,
            relation_type=relation_type,
            confidence_state=confidence_state,
            confidence_score=confidence_score,
            source=source,
        )
        self._dependencies.append(dep)
        return dep

    def get_dependencies_for_resource(self, resource_id: str) -> List[CyberDependencyDTO]:
        """Returns all direct upstream and downstream dependencies for a resource."""
        return [
            d for d in self._dependencies
            if d.source_id == resource_id or d.target_id == resource_id
        ]

    def build_graph(self) -> CyberDependencyGraphDTO:
        """Constructs aggregated graph representation."""
        node_ids = set()
        for d in self._dependencies:
            node_ids.add(d.source_id)
            node_ids.add(d.target_id)

        nodes = [{"id": nid, "label": nid} for nid in node_ids]
        unverified = len([d for d in self._dependencies if d.confidence_state in ("INFERRED", "UNKNOWN")])

        return CyberDependencyGraphDTO(
            nodes=nodes,
            edges=self._dependencies,
            total_dependencies=len(self._dependencies),
            unverified_count=unverified,
        )
