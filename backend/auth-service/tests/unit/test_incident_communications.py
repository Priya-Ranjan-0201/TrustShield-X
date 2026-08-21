import pytest
from app.services.soc.incident_communication_engine import IncidentCommunicationEngine


def test_incident_communication_sanitization():
    engine = IncidentCommunicationEngine()
    raw = "Containment finished. Attacker used Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    comm = engine.generate_update("inc_comm_01", "EXECUTIVE_UPDATE", raw)

    assert comm.audience == "EXECUTIVE_UPDATE"
    assert comm.label == "CONFIRMED"
    assert "Bearer [REDACTED_TOKEN]" in comm.content
    assert "eyJhbGci" not in comm.content
