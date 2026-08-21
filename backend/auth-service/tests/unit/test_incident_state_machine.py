import pytest
from app.services.soc.incident_state_machine import IncidentStateMachine


def test_incident_state_machine_legal_and_illegal_transitions():
    sm = IncidentStateMachine()
    inc = sm.init_incident("inc_state_01")
    assert inc.current_state == "NEW"

    # Legal: NEW -> TRIAGED -> INVESTIGATING
    t1 = sm.transition("inc_state_01", "TRIAGED")
    assert t1.current_state == "TRIAGED"
    t2 = sm.transition("inc_state_01", "INVESTIGATING")
    assert t2.current_state == "INVESTIGATING"

    # Illegal: INVESTIGATING -> CLOSED directly
    with pytest.raises(ValueError, match="Illegal state transition"):
        sm.transition("inc_state_01", "CLOSED")
