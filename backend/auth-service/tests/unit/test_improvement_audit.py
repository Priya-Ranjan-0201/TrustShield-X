import pytest
from app.services.security_engineering.incident_learning_engine import IncidentLearningEngine

def test_improvement_audit():
    engine = IncidentLearningEngine()
    learn = engine.record_incident_learning("inc_audit", "Det", "Resp", "Cont", "Rec")
    assert learn.learning_id.startswith("learn_")
