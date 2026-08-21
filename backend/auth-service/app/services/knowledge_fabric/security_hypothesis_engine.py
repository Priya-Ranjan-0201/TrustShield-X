"""
TruthShield X — Security Hypothesis Engine (Phase 19).

Generates and ranks competing hypotheses with evidence corroboration and identifies alternative explanations (AMBIGUOUS state).
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import SecurityHypothesisDTO


class SecurityHypothesisEngine:
    """Manages competing hypotheses for incident investigation."""

    def __init__(self):
        self._hypotheses: Dict[str, SecurityHypothesisDTO] = {}
        self._initialize_default_hypotheses()

    def _initialize_default_hypotheses(self):
        h1 = SecurityHypothesisDTO(
            hypothesis_id="hypo_cred_compromise",
            title="H1: Credential Compromise via Phishing",
            description="Service principal credentials were harvested through an MFA proxy attack.",
            supporting_evidence=["ev_pcap_trace_88", "ev_threat_intel_feed"],
            contradicting_evidence=[],
            confidence=0.88,
            rank=1,
        )
        h2 = SecurityHypothesisDTO(
            hypothesis_id="hypo_admin_anomaly",
            title="H2: Legitimate Out-of-Band Admin Activity",
            description="Authorized devops engineer performed scheduled emergency hotfix.",
            supporting_evidence=["ev_audit_log_90"],
            contradicting_evidence=["ev_threat_intel_feed"],
            confidence=0.45,
            rank=2,
            is_alternative_explanation=True,
        )
        self._hypotheses[h1.hypothesis_id] = h1
        self._hypotheses[h2.hypothesis_id] = h2

    def register_hypothesis(
        self,
        title: str,
        description: str,
        supporting_evidence: Optional[List[str]] = None,
        contradicting_evidence: Optional[List[str]] = None,
        confidence: float = 0.75,
        rank: int = 1,
        is_alternative_explanation: bool = False,
        is_ambiguous: bool = False,
    ) -> SecurityHypothesisDTO:
        hypo = SecurityHypothesisDTO(
            title=title,
            description=description,
            supporting_evidence=supporting_evidence or [],
            contradicting_evidence=contradicting_evidence or [],
            confidence=confidence,
            rank=rank,
            is_alternative_explanation=is_alternative_explanation,
            is_ambiguous=is_ambiguous,
        )
        self._hypotheses[hypo.hypothesis_id] = hypo
        return hypo

    def list_hypotheses(self) -> List[SecurityHypothesisDTO]:
        """Returns hypotheses ordered by rank."""
        return sorted(self._hypotheses.values(), key=lambda h: h.rank)
