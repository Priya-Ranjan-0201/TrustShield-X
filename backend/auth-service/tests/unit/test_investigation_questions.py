import pytest
from app.services.knowledge_fabric.investigation_question_engine import InvestigationQuestionEngine


def test_investigation_question_generation():
    engine = InvestigationQuestionEngine()
    questions = engine.list_prioritized_questions()

    assert len(questions) >= 2
    assert questions[0].priority_score >= questions[1].priority_score
