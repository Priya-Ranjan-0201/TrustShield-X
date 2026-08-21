"""
TruthShield X — Security Control Dependency Graph Engine
"""

from typing import Dict, List, Optional, Any


class ControlDependencyGraphEngine:
    """Models inter-control dependencies and identifies single points of security failure."""

    def __init__(self):
        # source_control_id -> List[dependent_control_ids]
        self._dependencies: Dict[str, List[str]] = {
            "ctrl_db_core": ["ctrl_audit_01", "ctrl_rbac_01", "ctrl_iso_01"],
            "ctrl_redis_cluster": ["ctrl_rate_limit_01", "ctrl_session_01"],
            "ctrl_waf_01": ["ctrl_edge_block_01", "ctrl_ddos_01"],
        }

    def get_dependencies(self, control_id: str) -> List[str]:
        """Returns dependent controls for a given source control."""
        return self._dependencies.get(control_id, [])

    def identify_single_points_of_failure(self) -> List[Dict[str, Any]]:
        """Identifies components whose failure cascades across 3 or more critical controls."""
        spofs = []
        for source_ctrl, dependents in self._dependencies.items():
            if len(dependents) >= 3:
                spofs = [{
                    "critical_component": source_ctrl,
                    "dependent_controls_count": len(dependents),
                    "dependent_controls": dependents,
                    "risk_classification": "SINGLE_POINT_OF_SECURITY_FAILURE",
                    "mitigation": "Deploy multi-AZ active-active standby redundancy.",
                }]
        return spofs
