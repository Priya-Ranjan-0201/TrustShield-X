import pytest
from app.services.security_engineering.incident_learning_engine import IncidentLearningEngine

def test_incident_learning():
    engine = IncidentLearningEngine()
    learn = engine.record_incident_learning(
        incident_id="inc_sample",
        detection_eval="Fired in 5s",
        response_eval="Contained in 30s",
        containment_eval="Effective",
        recovery_eval="No restore needed",
    )
    assert learn.incident_id == "inc_sample"
    assert len(learn.successful_controls) >= 1
