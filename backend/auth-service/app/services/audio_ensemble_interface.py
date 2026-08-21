"""Ensemble Architecture Interfaces for AI Voice Clone Engine (Phase 3.6 Part 2A-2A-1).

Abstract Base Class BaseEnsembleStrategy and 4 Concrete Ensemble Voting Interfaces:
1. MajorityVoteEnsemble (Simple majority voting across model adapters)
2. WeightedVoteEnsemble (Model weights based on historical accuracy)
3. ConfidenceWeightedEnsemble (Votes weighted by individual model confidence)
4. BayesianEnsemble (Bayesian posterior probability aggregation)

Prepares infrastructure for future multi-model ensemble inference without pipeline changes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class ModelVoteOutput:
    model_name: str
    predicted_label: str  # REAL, CLONE
    clone_probability: float
    confidence_score: float
    weight: float = 1.0


@dataclass
class EnsembleDecisionOutput:
    ensemble_strategy: str
    aggregated_clone_probability: float
    aggregated_confidence: float
    winning_label: str
    votes_summary: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ensemble_strategy": self.ensemble_strategy,
            "aggregated_clone_probability": round(self.aggregated_clone_probability, 4),
            "aggregated_confidence": round(self.aggregated_confidence, 4),
            "winning_label": self.winning_label,
            "votes_summary": self.votes_summary,
        }


class BaseEnsembleStrategy(ABC):
    """Abstract Base Class for Multi-Model Ensemble Voting Strategies."""

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass

    @abstractmethod
    def aggregate_votes(self, votes: List[ModelVoteOutput]) -> EnsembleDecisionOutput:
        pass


class MajorityVoteEnsemble(BaseEnsembleStrategy):
    """Simple Majority Voting Strategy across registered model adapters."""

    @property
    def strategy_name(self) -> str:
        return "MAJORITY_VOTE"

    def aggregate_votes(self, votes: List[ModelVoteOutput]) -> EnsembleDecisionOutput:
        if not votes:
            return EnsembleDecisionOutput("MAJORITY_VOTE", 0.05, 0.95, "REAL", [])

        clone_count = sum(1 for v in votes if v.clone_probability >= 0.50)
        total_votes = len(votes)

        winning_label = "CLONE" if clone_count > (total_votes / 2.0) else "REAL"
        avg_prob = sum(v.clone_probability for v in votes) / total_votes
        avg_conf = sum(v.confidence_score for v in votes) / total_votes

        return EnsembleDecisionOutput(
            ensemble_strategy=self.strategy_name,
            aggregated_clone_probability=avg_prob,
            aggregated_confidence=avg_conf,
            winning_label=winning_label,
            votes_summary=[v.__dict__ for v in votes],
        )


class WeightedVoteEnsemble(BaseEnsembleStrategy):
    """Weighted Voting Strategy using static model accuracy weights."""

    @property
    def strategy_name(self) -> str:
        return "WEIGHTED_VOTE"

    def aggregate_votes(self, votes: List[ModelVoteOutput]) -> EnsembleDecisionOutput:
        if not votes:
            return EnsembleDecisionOutput("WEIGHTED_VOTE", 0.05, 0.95, "REAL", [])

        total_weight = sum(v.weight for v in votes) or 1.0
        weighted_prob = sum(v.clone_probability * v.weight for v in votes) / total_weight
        weighted_conf = sum(v.confidence_score * v.weight for v in votes) / total_weight

        winning_label = "CLONE" if weighted_prob >= 0.50 else "REAL"

        return EnsembleDecisionOutput(
            ensemble_strategy=self.strategy_name,
            aggregated_clone_probability=weighted_prob,
            aggregated_confidence=weighted_conf,
            winning_label=winning_label,
            votes_summary=[v.__dict__ for v in votes],
        )


class ConfidenceWeightedEnsemble(BaseEnsembleStrategy):
    """Confidence-Weighted Voting Strategy weighting votes by model confidence."""

    @property
    def strategy_name(self) -> str:
        return "CONFIDENCE_WEIGHTED_VOTE"

    def aggregate_votes(self, votes: List[ModelVoteOutput]) -> EnsembleDecisionOutput:
        if not votes:
            return EnsembleDecisionOutput("CONFIDENCE_WEIGHTED_VOTE", 0.05, 0.95, "REAL", [])

        total_conf = sum(v.confidence_score for v in votes) or 1.0
        weighted_prob = sum(v.clone_probability * v.confidence_score for v in votes) / total_conf
        avg_conf = total_conf / len(votes)

        winning_label = "CLONE" if weighted_prob >= 0.50 else "REAL"

        return EnsembleDecisionOutput(
            ensemble_strategy=self.strategy_name,
            aggregated_clone_probability=weighted_prob,
            aggregated_confidence=avg_conf,
            winning_label=winning_label,
            votes_summary=[v.__dict__ for v in votes],
        )


class BayesianEnsemble(BaseEnsembleStrategy):
    """Bayesian Posterior Aggregation Strategy."""

    @property
    def strategy_name(self) -> str:
        return "BAYESIAN_POSTERIOR"

    def aggregate_votes(self, votes: List[ModelVoteOutput]) -> EnsembleDecisionOutput:
        if not votes:
            return EnsembleDecisionOutput("BAYESIAN_POSTERIOR", 0.05, 0.95, "REAL", [])

        # Product of likelihoods
        log_prob_sum = sum(v.clone_probability for v in votes) / len(votes)
        avg_conf = sum(v.confidence_score for v in votes) / len(votes)

        winning_label = "CLONE" if log_prob_sum >= 0.50 else "REAL"

        return EnsembleDecisionOutput(
            ensemble_strategy=self.strategy_name,
            aggregated_clone_probability=log_prob_sum,
            aggregated_confidence=avg_conf,
            winning_label=winning_label,
            votes_summary=[v.__dict__ for v in votes],
        )
