import pytest
from app.services.knowledge_fabric.investigation_question_engine import InvestigationQuestionEngine


def test_knowledge_driven_threat_hunting_hypotheses():
    engine = InvestigationQuestionEngine()
    q = engine.add_question(
        question="Hunt for unlinked service account access from external IPs.",
        target_entity="usr_admin_svc",
        expected_information_gain=0.95,
        risk_reduction_impact=0.90,
    )

    assert q.target_entity == "usr_admin_svc"
    assert q.priority_score > 0.90
