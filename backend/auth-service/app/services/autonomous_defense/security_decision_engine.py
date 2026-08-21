"""
TruthShield X — Security Decision Engine (Phase 30).

Records and evaluates transparent, evidence-grounded security decisions with explicit rationale and confidence.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.schemas.autonomous_defense_models import SecurityDecisionRecordDTO, DecisionTypeLiteral, AutonomyLevelLiteral


class SecurityDecisionEngine:
    """Manages explainable decision records across all autonomous defense modules."""

    def __init__(self):
        self._decisions: Dict[str, SecurityDecisionRecordDTO] = {}
        self._seed_default_decisions()

    def _seed_default_decisions(self):
        d1 = SecurityDecisionRecordDTO(
            decision_id="dec_waf_containment_01",
            decision_type="RESPONSE_RECOMMENDATION",
            actor_type="AUTONOMOUS_ENGINE",
            actor_id="engine_response_opt_01",
            evidence=["Sigma alert C2 burst", "Digital Twin sandbox simulation 85% containment"],
            context={"threat": "DarkStorm", "target": "ast_api_gw"},
            policy="POL-AUTONOMOUS-CONTAINMENT-V2",
            recommendation="Apply dynamic rate-limiting on Edge Gateway",
            confidence=0.94,
            selected_action="WAF_RATE_LIMIT",
            alternatives=["FULL_ISOLATION", "PASSIVE_MONITORING"],
            expected_outcome="90% reduction in malicious credential-stuffing traffic without dropping benign users",
            actual_outcome=None,
            verification_status="SIMULATED",
            approval="USR_CISO_FOUR_EYES",
            rollback_plan="Revert WAF rate-limit ruleset to baseline",
            autonomy_level="LEVEL_4",
            tenant_id="default_tenant",
        )
        self._decisions[d1.decision_id] = d1

    def create_decision(
        self,
        decision_type: DecisionTypeLiteral,
        recommendation: str,
        evidence: List[str],
        confidence: float,
        selected_action: str,
        expected_outcome: str,
        policy: str = "POL-DEFAULT-SECURITY",
        alternatives: Optional[List[str]] = None,
        rollback_plan: str = "Revert to baseline",
        autonomy_level: AutonomyLevelLiteral = "LEVEL_4",
        tenant_id: str = "default_tenant",
    ) -> SecurityDecisionRecordDTO:
        dto = SecurityDecisionRecordDTO(
            decision_type=decision_type,
            actor_type="AUTONOMOUS_ENGINE",
            actor_id="autonomous_decision_engine",
            evidence=evidence,
            context={"tenant": tenant_id},
            policy=policy,
            recommendation=recommendation,
            confidence=confidence,
            selected_action=selected_action,
            alternatives=alternatives or ["DO_NOTHING"],
            expected_outcome=expected_outcome,
            actual_outcome=None,
            verification_status="CANDIDATE",
            approval=None,
            rollback_plan=rollback_plan,
            autonomy_level=autonomy_level,
            tenant_id=tenant_id,
        )
        self._decisions[dto.decision_id] = dto
        return dto

    def get_decision(self, decision_id: str) -> Optional[SecurityDecisionRecordDTO]:
        return self._decisions.get(decision_id)

    def list_decisions(self, tenant_id: str = "default_tenant") -> List[SecurityDecisionRecordDTO]:
        return [d for d in self._decisions.values() if d.tenant_id == tenant_id]

    def explain_decision(self, decision_id: str) -> Dict[str, Any]:
        d = self.get_decision(decision_id)
        if not d:
            raise ValueError(f"Decision '{decision_id}' not found.")

        return {
            "decision_id": d.decision_id,
            "why": d.recommendation,
            "evidence": d.evidence,
            "policy": d.policy,
            "alternatives": d.alternatives,
            "confidence": d.confidence,
            "limitations": "Requires live production outcome verification before learning.",
            "rollback_plan": d.rollback_plan,
        }
