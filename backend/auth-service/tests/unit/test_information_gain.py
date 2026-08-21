import pytest
from app.services.knowledge_fabric.investigation_question_engine import InvestigationQuestionEngine


def test_information_gain_prioritization():
    engine = InvestigationQuestionEngine()

    q_high = engine.add_question(
        question="Is root access currently active on database?",
        target_entity="db_primary_users",
        expected_information_gain=0.98,
        risk_reduction_impact=0.95,
    )

    q_low = engine.add_question(
        question="What is the server casing serial number?",
        target_entity="db_primary_users",
        expected_information_gain=0.10,
        risk_reduction_impact=0.05,
    )

    assert q_high.priority_score > q_low.priority_score
    questions = engine.list_prioritized_questions()
    assert questions[0].question_id == q_high.question_id
