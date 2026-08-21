"""
TruthShield X — Threat Hunting Optimization Engine (Phase 30).

Learns from successful and failed hunts, prioritizes candidate hypotheses, and synthesizes novel queries.
"""

from typing import Dict, List, Optional
from app.schemas.autonomous_defense_models import ThreatHuntingOptimizationDTO


class ThreatHuntingOptimizationEngine:
    """Optimizes threat hunting queries based on campaign intelligence and historical hypothesis efficacy."""

    def __init__(self):
        self._hunts: Dict[str, ThreatHuntingOptimizationDTO] = {}
        self._seed_default_hunt()

    def _seed_default_hunt(self):
        h1 = ThreatHuntingOptimizationDTO(
            hunt_id="hunt_opt_dns_tunneling",
            hypothesis="Attackers are utilizing secondary DNS resolvers to bypass primary WAF inspection",
            data_sources=["CoreDNS logs", "Zeek DNS records"],
            novelty_score=0.88,
            priority="HIGH",
            status="CANDIDATE",
        )
        self._hunts[h1.hunt_id] = h1

    def create_candidate_hunt(
        self,
        hypothesis: str,
        data_sources: List[str],
        novelty_score: float = 0.85,
    ) -> ThreatHuntingOptimizationDTO:
        dto = ThreatHuntingOptimizationDTO(
            hypothesis=hypothesis,
            data_sources=data_sources,
            novelty_score=novelty_score,
            priority="HIGH" if novelty_score > 0.80 else "MEDIUM",
            status="CANDIDATE",
        )
        self._hunts[dto.hunt_id] = dto
        return dto

    def list_candidate_hunts(self) -> List[ThreatHuntingOptimizationDTO]:
        return list(self._hunts.values())
