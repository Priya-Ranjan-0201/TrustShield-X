import pytest
from app.services.ai_governance.ai_incident_response_engine import AIIncidentResponseEngine

def test_model_kill_switch_disable():
    engine = AIIncidentResponseEngine()
    res = engine.emergency_kill_switch("mdl_c2_neural_classifier", "usr_ciso_alpha")
    assert res["status"] == "MODEL_DISABLE"
    assert res["serving_state"] == "TERMINATED"
