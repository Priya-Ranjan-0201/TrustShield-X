import pytest
from app.services.cyber_crisis_command.crisis_recovery_engine import CrisisRecoveryEngine

def test_recovery_task_creation():
    engine = CrisisRecoveryEngine()
    task = engine.create_recovery_task("REC-01", "C-01", "t1", "Re-image host", "APPLICATION", "DevOps")
    assert task["status"] == "NOT_STARTED"
    assert task["task_id"] == "REC-01"
