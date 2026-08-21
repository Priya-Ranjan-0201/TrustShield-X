"""
TruthShield X — Resilience Improvement Roadmap Engine (Phase 18).

Generates prioritized NOW / NEXT / LATER roadmaps referencing simulation evidence.
"""

from typing import List, Dict, Optional
from app.schemas.cyber_resilience_twin_models import (
    ResilienceRecommendationDTO,
    ResilienceImprovementRoadmapDTO,
)


class ResilienceRoadmapEngine:
    """Prioritizes resilience initiatives across temporal stages."""

    def __init__(self):
        self._recommendations: List[ResilienceRecommendationDTO] = []
        self._initialize_default_recommendations()

    def _initialize_default_recommendations(self):
        defaults = [
            ResilienceRecommendationDTO(
                title="Deploy Redundant Replica for Shared Auth Service (Eliminate SPOF)",
                target_resource="service_auth_jwt",
                risk_reduction_impact=85.0,
                implementation_effort="LOW",
                stage="NOW",
                evidence_references=["spof_dep_auth_01"],
            ),
            ResilienceRecommendationDTO(
                title="Enforce Micro-Segmentation between Ingress DMZ and Database Tier",
                target_resource="vpc-prod-dmz",
                risk_reduction_impact=70.0,
                implementation_effort="MEDIUM",
                stage="NEXT",
                evidence_references=["scen_ransomware_01"],
            ),
            ResilienceRecommendationDTO(
                title="Automate Disaster Recovery DNS Failover Health Checks",
                target_resource="dns_dr_failover_record",
                risk_reduction_impact=60.0,
                implementation_effort="HIGH",
                stage="LATER",
                evidence_references=["dr_bottleneck_wal_01"],
            ),
        ]
        self._recommendations.extend(defaults)

    def generate_roadmap(self) -> ResilienceImprovementRoadmapDTO:
        """Categorizes recommendations into NOW, NEXT, and LATER roadmap stages."""
        now = [r for r in self._recommendations if r.stage == "NOW"]
        next_stage = [r for r in self._recommendations if r.stage == "NEXT"]
        later = [r for r in self._recommendations if r.stage == "LATER"]

        return ResilienceImprovementRoadmapDTO(
            now_actions=now,
            next_actions=next_stage,
            later_actions=later,
            total_actions=len(self._recommendations),
        )

    def add_recommendation(self, rec: ResilienceRecommendationDTO):
        self._recommendations.append(rec)
