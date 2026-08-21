import pytest
from app.services.ai_governance.ai_incident_response_engine import AIIncidentResponseEngine

def test_ai_incident_response_listing():
    engine = AIIncidentResponseEngine()
    incidents = engine.list_incidents("default_tenant")
    assert len(incidents) >= 1
    assert incidents[0].attack_type == "PROMPT_INJECTION"
