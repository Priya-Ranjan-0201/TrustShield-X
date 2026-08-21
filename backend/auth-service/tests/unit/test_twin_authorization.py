import pytest
from app.services.resilience_twin.simulation_safety_sandbox import SimulationSafetySandbox


def test_twin_authorization_cancellation_privilege():
    sandbox = SimulationSafetySandbox()
    sandbox.cancel_simulation("sim_999", "Admin emergency override")

    assert sandbox.is_cancelled("sim_999") is True
