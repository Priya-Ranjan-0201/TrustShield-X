"""
TruthShield X — Decision Traceability Engine (Phase 19).

Captures full provenance of security decisions answering:
- What knowledge led to this?
- What evidence?
- What policy?
- What alternatives?
- Who/what decided?
- What happened afterward?
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import DecisionTraceabilityDTO


class DecisionTraceabilityEngine:
    """Manages decision traceability logs."""

    def __init__(self):
        self._decisions: Dict[str, DecisionTraceabilityDTO] = {}
        self._initialize_default_decision()

    def _initialize_default_decision(self):
        d = DecisionTraceabilityDTO(
            decision_id="dec_quarantine_01",
            decision_type="DEFENSIVE_QUARANTINE",
            driving_knowledge=["kobj_cve_2026_9942", "kobj_srv_checkout_production"],
            supporting_evidence=["ev_pcap_trace_88", "ev_vuln_scan_44"],
            governing_policy="POL_SEC_AUTO_ISOLATION_CRITICAL",
            alternative_options=["RATE_LIMIT_ONLY", "LOG_ONLY"],
            decision_maker="AUTONOMOUS_POLICY_AGENT_V2",
            post_action_outcome="Lateral communication dropped with zero checkout customer checkout failures.",
        )
        self._decisions[d.decision_id] = d

    def record_decision(
        self,
        decision_type: str,
        driving_knowledge: List[str],
        supporting_evidence: List[str],
        governing_policy: str,
        alternative_options: List[str],
        decision_maker: str,
        post_action_outcome: Optional[str] = None,
    ) -> DecisionTraceabilityDTO:
        decision = DecisionTraceabilityDTO(
            decision_type=decision_type,
            driving_knowledge=driving_knowledge,
            supporting_evidence=supporting_evidence,
            governing_policy=governing_policy,
            alternative_options=alternative_options,
            decision_maker=decision_maker,
            post_action_outcome=post_action_outcome,
        )
        self._decisions[decision.decision_id] = decision
        return decision

    def get_decision(self, decision_id: str) -> Optional[DecisionTraceabilityDTO]:
        return self._decisions.get(decision_id)

    def list_decisions(self) -> List[DecisionTraceabilityDTO]:
        return list(self._decisions.values())
