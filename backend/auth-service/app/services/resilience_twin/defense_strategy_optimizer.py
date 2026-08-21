"""
TruthShield X — Defense Strategy Optimizer & Pareto Frontier Engine (Phase 18).

Optimizes defense options by calculating Pareto-efficient trade-offs between risk reduction and service availability.
"""

from typing import List
from app.schemas.cyber_resilience_twin_models import DefenseStrategyCandidateDTO


class DefenseStrategyOptimizer:
    """Computes Pareto frontier for candidate defense strategies."""

    def optimize_strategies(self, candidates: List[DefenseStrategyCandidateDTO]) -> List[DefenseStrategyCandidateDTO]:
        """Identifies non-dominated Pareto optimal defense candidates."""
        if not candidates:
            return []

        # A candidate is Pareto-optimal if no other candidate has BOTH higher risk reduction AND lower service disruption/cost
        for c in candidates:
            is_dominated = False
            for other in candidates:
                if other.strategy_id == c.strategy_id:
                    continue

                # 'other' dominates 'c' if it is strictly better in one and not worse in others
                if (other.risk_reduction >= c.risk_reduction and
                    other.service_disruption <= c.service_disruption and
                    other.implementation_cost <= c.implementation_cost and
                    (other.risk_reduction > c.risk_reduction or
                     other.service_disruption < c.service_disruption or
                     other.implementation_cost < c.implementation_cost)):
                    is_dominated = True
                    break

            c.is_pareto_optimal = not is_dominated

        return candidates
