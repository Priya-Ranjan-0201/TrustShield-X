import pytest
from app.services.cyber_crisis_command.crisis_recovery_engine import CrisisRecoveryEngine

def test_candidate_lessons_learned_generation():
    engine = CrisisRecoveryEngine()
    lessons = engine.generate_candidate_lessons_learned("C-01", "t1", [{"event": "Test"}])
    assert len(lessons) >= 2
    assert all("CANDIDATE" in l["status"] for l in lessons)
