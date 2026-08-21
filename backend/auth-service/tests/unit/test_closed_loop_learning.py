import pytest
from app.services.soc.closed_loop_learning_engine import ClosedLoopLearningEngine


def test_closed_loop_learning_divergence_analysis():
    engine = ClosedLoopLearningEngine()
    lessons = engine.extract_lessons(
        incident_id="inc_learn_01",
        expected_state="FIREWALL_DROP",
        actual_state="FIREWALL_ALLOW_ACTIVE",
        mttd_minutes=18.5,
    )

    assert lessons["divergence_from_expected"] is True
    assert lessons["detection_gap_detected"] is True
    assert len(lessons["recommended_improvements"]) >= 2
