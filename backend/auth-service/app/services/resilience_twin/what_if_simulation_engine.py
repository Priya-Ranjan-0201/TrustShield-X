"""
TruthShield X — What-If Simulation Engine (Phase 18).

Simulates counterfactual hypothesis queries against the Digital Security Twin.
"""

from typing import Dict, Any
from app.schemas.cyber_resilience_twin_models import (
    WhatIfQueryDTO,
    WhatIfResultDTO,
)
from app.services.resilience_twin.cyber_dependency_graph_engine import CyberDependencyGraphEngine


class WhatIfSimulationEngine:
    """Evaluates counterfactual security hypotheses and blast radii."""

    def __init__(self, dep_engine: CyberDependencyGraphEngine):
        self.dep_engine = dep_engine

    def simulate_what_if(self, query: WhatIfQueryDTO) -> WhatIfResultDTO:
        """Executes what-if query hypothesis simulation."""
        deps = self.dep_engine.get_dependencies_for_resource(query.target_resource)
        affected_services = [d.source_id for d in deps if d.target_id == query.target_resource]
        if not affected_services:
            affected_services = [query.target_resource]

        # Calculate estimated blast radius
        blast_radius = max(1, len(affected_services) + 1)
        base_risk = 25.0
        if query.query_type in ("CONTROL_FAILURE", "ASSET_COMPROMISE"):
            est_risk = min(100.0, base_risk + (blast_radius * 12.0))
        elif query.query_type == "DEFENSE_ACTIVATION":
            est_risk = max(5.0, base_risk - 15.0)
        else:
            est_risk = 45.0

        return WhatIfResultDTO(
            target_resource=query.target_resource,
            simulated_change=query.simulated_change,
            blast_radius_asset_count=blast_radius,
            affected_services=affected_services,
            estimated_residual_risk=round(est_risk, 1),
            label="SIMULATED",
            is_simulated=True,
        )
