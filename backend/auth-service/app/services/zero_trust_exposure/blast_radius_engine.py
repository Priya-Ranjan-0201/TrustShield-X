"""
Blast Radius Reduction & Lateral Movement Simulation Engine (Phase 34)
======================================================================
Models attacker pivot vectors, credentials reuse paths, network reachability,
and quantifies potential compromise explosion bounds to recommend containment chokepoints.
"""

from typing import Dict, Any, List, Optional
import datetime


class BlastRadiusEngine:
    def __init__(self):
        self._simulations: Dict[str, Dict[str, Any]] = {}

    def simulate_compromise(
        self,
        simulation_id: str,
        tenant_id: str,
        initial_compromised_node: str,
        network_neighbors: List[str],
        accessible_data_stores: List[str],
        assumed_credentials_scope: str = "LOCAL"
    ) -> Dict[str, Any]:
        # Calculate blast radius impact
        scope_multiplier = 2.0 if assumed_credentials_scope == "GLOBAL_ADMIN" else 1.0
        affected_nodes_count = len(network_neighbors) + len(accessible_data_stores)
        blast_radius_score = min(10.0, affected_nodes_count * scope_multiplier * 1.5)

        recommended_isolations = [
            f"MICROSEGMENT_NODE_{initial_compromised_node}",
            f"REVOKE_CREDENTIALS_{initial_compromised_node}"
        ]
        if accessible_data_stores:
            recommended_isolations.append(f"RESTRICT_DATASTORE_ACCESS_{accessible_data_stores[0]}")

        simulation = {
            "simulation_id": simulation_id,
            "tenant_id": tenant_id,
            "initial_node": initial_compromised_node,
            "potential_lateral_nodes": network_neighbors,
            "at_risk_data_stores": accessible_data_stores,
            "blast_radius_score": blast_radius_score,
            "recommended_containment_actions": recommended_isolations,
            "simulated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        self._simulations[simulation_id] = simulation
        return simulation

    def calculate_blast_radius(
        self,
        node_id: str,
        tenant_id: str,
        neighbors: Optional[List[str]] = None,
        data_stores: Optional[List[str]] = None,
        credentials_scope: str = "LOCAL"
    ) -> Dict[str, Any]:
        sim_id = f"sim_{node_id}_{datetime.datetime.now(datetime.timezone.utc).timestamp()}"
        return self.simulate_compromise(
            simulation_id=sim_id,
            tenant_id=tenant_id,
            initial_compromised_node=node_id,
            network_neighbors=neighbors or [],
            accessible_data_stores=data_stores or [],
            assumed_credentials_scope=credentials_scope
        )

    def get_simulation_history(self, tenant_id: str) -> List[Dict[str, Any]]:
        return [s for s in self._simulations.values() if s["tenant_id"] == tenant_id]


blast_radius_engine = BlastRadiusEngine()
