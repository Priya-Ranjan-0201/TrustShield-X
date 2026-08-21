"""
TruthShield X — Hypothesis Challenge & Anti-Confirmation-Bias Engine
"""

from typing import Dict, List, Optional, Any
from app.schemas.hunting_models import ThreatHuntHypothesisDTO, HuntConclusionLiteral


class HypothesisChallengeEngine:
    """Actively challenges hunt hypotheses, evaluates counter-evidence, and prevents false confirmation bias."""

    def challenge_hypothesis(
        self,
        hypothesis: ThreatHuntHypothesisDTO,
        observed_facts: List[Dict[str, Any]],
        known_counter_evidence: Optional[List[Dict[str, Any]]] = None,
    ) -> ThreatHuntHypothesisDTO:
        """Evaluates supporting evidence against counter-evidence to produce an objective, balanced conclusion."""
        supp_count = len(hypothesis.supporting_evidence) + len(observed_facts)
        counter = known_counter_evidence or []
        counter_count = len(hypothesis.counter_evidence) + len(counter)

        hypothesis.evidence_count = supp_count + counter_count
        if counter:
            hypothesis.counter_evidence.extend(counter)

        # Baseline confidence calculation
        base_confidence = 0.50 + (supp_count * 0.10)
        # Anti-bias discount: counter-evidence aggressively penalizes confidence
        counter_penalty = counter_count * 0.25
        calibrated_confidence = max(0.10, min(0.99, base_confidence - counter_penalty))
        hypothesis.confidence = round(calibrated_confidence, 2)

        # Objective Conclusion Evaluation
        conclusion: HuntConclusionLiteral = "INSUFFICIENT_EVIDENCE"

        if counter_count > 0 and counter_count >= supp_count:
            conclusion = "REFUTED" if counter_count > supp_count else "INCONCLUSIVE"
            hypothesis.status = "REFUTED" if conclusion == "REFUTED" else "INCONCLUSIVE"
        elif supp_count >= 3 and calibrated_confidence >= 0.80:
            conclusion = "THREAT_CONFIRMED"
            hypothesis.status = "SUPPORTED"
        elif supp_count >= 1 and calibrated_confidence >= 0.60:
            conclusion = "THREAT_SUPPORTED"
            hypothesis.status = "SUPPORTED"
        elif supp_count > 0:
            conclusion = "SUSPICIOUS"
            hypothesis.status = "INVESTIGATING"

        hypothesis.conclusion = conclusion
        return hypothesis

    def generate_alternative_explanations(
        self,
        hypothesis_type: str,
        observed_phenomenon: str,
    ) -> List[str]:
        """Generates plausible competing alternative explanations for an anomaly."""
        return [
            f"Legitimate administrative or infrastructure migration ({observed_phenomenon}).",
            "Third-party vendor maintenance or scheduled certificate renewal.",
            "Opportunistic benign scanner activity without malicious targeting.",
            "Adversarial campaign expansion or staging infrastructure.",
        ]
