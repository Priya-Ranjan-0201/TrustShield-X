import pytest
from app.services.ai_governance.ai_incident_response_engine import AIIncidentResponseEngine

def test_model_quarantine_action():
    engine = AIIncidentResponseEngine()
    res = engine.trigger_model_quarantine("mdl_c2_neural_classifier", "Severe drift detected")
    assert res["status"] == "MODEL_QUARANTINED"
    assert res["action"] == "SERVING_BLOCKED_IMMEDIATELY"
