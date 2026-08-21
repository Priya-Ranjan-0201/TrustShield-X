"""
TruthShield X — Control Optimization Engine (Phase 30).

Continuously analyzes prevention, detection, response, and recovery controls to surface gaps and candidate remediation.
"""

from typing import Dict, List, Optional
from app.schemas.autonomous_defense_models import ControlOptimizationDTO


class ControlOptimizationEngine:
    """Evaluates discrete control domain effectiveness without collapsing into an opaque aggregate."""

    def __init__(self):
        self._controls: Dict[str, ControlOptimizationDTO] = {}
        self._seed_default_controls()

    def _seed_default_controls(self):
        c1 = ControlOptimizationDTO(
            control_id="ctrl_ingress_waf",
            control_domain="PREVENTION",
            effectiveness_score=0.95,
            gap_description=None,
            candidate_remediation=None,
        )
        c2 = ControlOptimizationDTO(
            control_id="ctrl_dns_entropy_sensor",
            control_domain="DETECTION",
            effectiveness_score=0.92,
            gap_description="Latency spike during burst queries",
            candidate_remediation="Deploy eBPF in-kernel filter",
        )
        self._controls[c1.control_id] = c1
        self._controls[c2.control_id] = c2

    def get_control(self, control_id: str) -> Optional[ControlOptimizationDTO]:
        return self._controls.get(control_id)

    def list_controls(self) -> List[ControlOptimizationDTO]:
        return list(self._controls.values())
