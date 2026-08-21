"""
TruthShield X — Master Autonomous Threat Hunting Fabric
"""

import uuid
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.hunting_models import (
    ThreatHuntHypothesisDTO,
    ThreatHuntResultDTO,
    HuntBudgetConfigDTO,
    HypothesisTypeLiteral,
)
from app.services.hunting.threat_hunt_query_engine import ThreatHuntQueryEngine
from app.services.hunting.hypothesis_challenge_engine import HypothesisChallengeEngine
from app.services.hunting.attack_path_reasoning_engine import AttackPathReasoningEngine
from app.services.hunting.predictive_defense_engine import PredictiveDefenseEngine
from app.services.hunting.early_warning_engine import EarlyWarningEngine


class ThreatHuntingFabric:
    """Master orchestration layer for autonomous threat discovery, bounded execution, and attack-path hypothesis testing."""

    def __init__(
        self,
        query_engine: Optional[ThreatHuntQueryEngine] = None,
        challenge_engine: Optional[HypothesisChallengeEngine] = None,
        attack_path_engine: Optional[AttackPathReasoningEngine] = None,
        predictive_engine: Optional[PredictiveDefenseEngine] = None,
        early_warning_engine: Optional[EarlyWarningEngine] = None,
    ):
        self.query = query_engine or ThreatHuntQueryEngine()
        self.challenge = challenge_engine or HypothesisChallengeEngine()
        self.attack_paths = attack_path_engine or AttackPathReasoningEngine()
        self.predictive = predictive_engine or PredictiveDefenseEngine()
        self.early_warning = early_warning_engine or EarlyWarningEngine()

        # hypothesis_id -> ThreatHuntHypothesisDTO
        self._hypotheses: Dict[str, ThreatHuntHypothesisDTO] = {}
        # result_id -> ThreatHuntResultDTO
        self._results: Dict[str, ThreatHuntResultDTO] = {}

    def create_hunt_hypothesis(
        self,
        title: str,
        description: str,
        hypothesis_type: HypothesisTypeLiteral = "CAMPAIGN_EXPANSION",
        target_assets: Optional[List[str]] = None,
        initial_evidence: Optional[List[Dict[str, Any]]] = None,
        tenant_id: str = "default_tenant",
    ) -> ThreatHuntHypothesisDTO:
        """Initializes a new structured hunt hypothesis."""
        hyp_id = f"hpt_{uuid.uuid4().hex[:10]}"
        hyp = ThreatHuntHypothesisDTO(
            hypothesis_id=hyp_id,
            tenant_id=tenant_id,
            title=title,
            description=description,
            hypothesis_type=hypothesis_type,
            status="ACTIVE",
            priority="HIGH",
            confidence=0.70,
            supporting_evidence=initial_evidence or [],
            counter_evidence=[],
            assumptions=["Initial anomalous telemetry links to active external campaign indicators."],
            alternative_hypotheses=self.challenge.generate_alternative_explanations(hypothesis_type, title),
            target_assets=target_assets or [],
        )

        self._hypotheses[hyp_id] = hyp
        return hyp

    def run_bounded_hunt(
        self,
        hypothesis_id: str,
        budget: Optional[HuntBudgetConfigDTO] = None,
        known_counter_evidence: Optional[List[Dict[str, Any]]] = None,
    ) -> ThreatHuntResultDTO:
        """Executes the complete autonomous hunt loop within deterministic resource budgets."""
        hyp = self._hypotheses.get(hypothesis_id)
        if not hyp:
            raise KeyError(f"Hypothesis '{hypothesis_id}' not found.")

        cfg = budget or HuntBudgetConfigDTO()

        # 1. Search telemetry via Query Engine
        records = self.query.execute_hunt_query(
            dsl_query=f"FIND assets WHERE exposure_score > 40",
            tenant_id=hyp.tenant_id,
            max_results=cfg.max_records_to_scan,
        )

        # 2. Challenge hypothesis with anti-confirmation-bias engine
        self.challenge.challenge_hypothesis(hyp, records, known_counter_evidence=known_counter_evidence)

        # 3. Construct attack paths
        paths = []
        for asset in (hyp.target_assets or ["TargetCorpGateway"]):
            path = self.attack_paths.construct_attack_path(
                entry_point="ObservedSuspiciousDNS",
                target_asset=asset,
                campaign_name="CAMP-2026-0891",
            )
            paths.append(path)

        # 4. Generate recommendations
        recs = [
            f"Review security headers and verify certificate fingerprints on {', '.join(hyp.target_assets or ['targets'])}.",
            "Enforce WAF rate limiting on suspect incoming IP subnets.",
            "Compare current asset configurations against verified golden baselines.",
        ]

        result_id = f"res_{uuid.uuid4().hex[:10]}"
        res = ThreatHuntResultDTO(
            result_id=result_id,
            hypothesis_id=hyp.hypothesis_id,
            conclusion=hyp.conclusion or "INSUFFICIENT_EVIDENCE",
            confidence=hyp.confidence,
            supporting_evidence=hyp.supporting_evidence,
            counter_evidence=hyp.counter_evidence,
            affected_assets=hyp.target_assets,
            related_campaigns=["CAMP-2026-0891"],
            attack_paths=paths,
            recommendations=recs,
            limitations=["Hunt restricted to passive observations; no active invasive probing performed."],
        )

        self._results[result_id] = res
        return res

    def cancel_hunt(self, hypothesis_id: str, reason: str) -> ThreatHuntHypothesisDTO:
        """Cancels an active hunt preserving partial evidence."""
        hyp = self._hypotheses.get(hypothesis_id)
        if not hyp:
            raise KeyError(f"Hypothesis '{hypothesis_id}' not found.")

        hyp.status = "CLOSED"
        hyp.conclusion = "INSUFFICIENT_EVIDENCE"
        hyp.assumptions.append(f"Canceled by operator: {reason}")
        return hyp

    def list_hypotheses(self, tenant_id: str = "default_tenant") -> List[ThreatHuntHypothesisDTO]:
        """Lists threat hunt hypotheses for tenant."""
        return [h for h in self._hypotheses.values() if h.tenant_id == tenant_id]
