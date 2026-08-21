import pytest
from app.services.soc.incident_command_engine import IncidentCommandEngine


def test_soc_rbac_command_roles():
    engine = IncidentCommandEngine()
    cmd = engine.assign_command_team(
        incident_id="inc_rbac",
        commander="usr_ciso",
        technical_lead="usr_eng",
        comms_lead="usr_comms",
        recovery_lead="usr_sre",
        security_analyst="usr_analyst",
    )

    assert cmd.incident_commander == "usr_ciso"
    assert cmd.security_analyst == "usr_analyst"
