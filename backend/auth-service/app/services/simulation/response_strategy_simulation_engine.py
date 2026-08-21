"""
TruthShield X — Response Strategy Simulation & Safety Scoring Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.simulation_models import ResponseStrategyComparisonDTO


class ResponseStrategySimulationEngine:
    """Evaluates and scores response strategies within the Digital Security Twin prior to production execution."""

    @staticmethod
    def calculate_safety_score(
        reversibility: str,
        operational_impact: str,
        simulated_blast_radius: str,
        confidence: float,
    ) -> float:
        """Calculates a normalized safety score in [0.0, 1.0]."""
        base = 0.50

        # Reversibility factor
        if reversibility == "HIGH":
            base += 0.25
        elif reversibility == "MEDIUM":
            base += 0.10

        # Operational impact penalty
        if operational_impact == "LOW":
            base += 0.15
        elif operational_impact == "HIGH":
            base -= 0.20

        # Blast radius adjustment
        if simulated_blast_radius == "MINIMAL":
            base += 0.10
        elif simulated_blast_radius == "EXTENSIVE":
            base -= 0.15

        # Weighted by confidence
        final_score = base * confidence
        return round(max(0.10, min(0.99, final_score)), 2)

    def evaluate_strategies(
        self,
        incident_context: Dict[str, Any],
    ) -> List[ResponseStrategyComparisonDTO]:
        """Compares multiple response candidates and returns detailed tradeoff metrics."""
        return [
            ResponseStrategyComparisonDTO(
                strategy_id="strat_iso_01",
                strategy_name="Isolate Compromised Host",
                action_type="ISOLATE_ASSET",
                simulated_risk_reduction=40.0,
                simulated_exposure_reduction=45.0,
                simulated_blast_radius="MINIMAL",
                operational_impact="MEDIUM",
                reversibility="HIGH",
                safety_score=self.calculate_safety_score("HIGH", "MEDIUM", "MINIMAL", 0.95),
                confidence=0.95,
                recommendation="Safest immediate containment with guaranteed one-click rollback.",
            ),
            ResponseStrategyComparisonDTO(
                strategy_id="strat_block_01",
                strategy_name="Block External C2 IP on Perimeter WAF",
                action_type="BLOCK_INDICATOR",
                simulated_risk_reduction=25.0,
                simulated_exposure_reduction=30.0,
                simulated_blast_radius="MINIMAL",
                operational_impact="LOW",
                reversibility="HIGH",
                safety_score=self.calculate_safety_score("HIGH", "LOW", "MINIMAL", 0.98),
                confidence=0.98,
                recommendation="Low-risk perimeter defense preventing C2 callback.",
            ),
        ]
