"""
TruthShield X — Investigation Question Engine (Phase 19).

Generates and prioritizes high-value investigation questions based on expected information gain and risk reduction.
"""

from typing import Dict, List, Optional
from app.schemas.cyber_knowledge_fabric_models import InvestigationQuestionDTO


class InvestigationQuestionEngine:
    """Manages investigation questions prioritized by information gain."""

    def __init__(self):
        self._questions: Dict[str, InvestigationQuestionDTO] = {}
        self._initialize_default_questions()

    def _initialize_default_questions(self):
        q1 = InvestigationQuestionDTO(
            question_id="iq_auth_token",
            question="Which identity principal generated the outbound TCP connection to IP 198.51.100.42?",
            target_entity="srv_checkout_production",
            expected_information_gain=0.92,
            risk_reduction_impact=0.88,
            urgency="CRITICAL",
            feasibility="EASY",
            priority_score=0.95,
        )
        q2 = InvestigationQuestionDTO(
            question_id="iq_waf_bypass",
            question="Was the WAF edge rule bypassed using chunked HTTP transfer encoding?",
            target_entity="ctrl_waf_edge_01",
            expected_information_gain=0.85,
            risk_reduction_impact=0.80,
            urgency="HIGH",
            feasibility="MODERATE",
            priority_score=0.86,
        )
        self._questions[q1.question_id] = q1
        self._questions[q2.question_id] = q2

    def add_question(
        self,
        question: str,
        target_entity: str,
        expected_information_gain: float = 0.85,
        risk_reduction_impact: float = 0.80,
        urgency: str = "HIGH",
        feasibility: str = "EASY",
    ) -> InvestigationQuestionDTO:
        # Calculate priority score
        score = round((expected_information_gain * 0.5) + (risk_reduction_impact * 0.5), 4)
        iq = InvestigationQuestionDTO(
            question=question,
            target_entity=target_entity,
            expected_information_gain=expected_information_gain,
            risk_reduction_impact=risk_reduction_impact,
            urgency=urgency,  # type: ignore
            feasibility=feasibility,  # type: ignore
            priority_score=score,
        )
        self._questions[iq.question_id] = iq
        return iq

    def list_prioritized_questions(self) -> List[InvestigationQuestionDTO]:
        return sorted(self._questions.values(), key=lambda q: q.priority_score, reverse=True)
