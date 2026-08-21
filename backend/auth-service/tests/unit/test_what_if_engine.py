import pytest
from app.services.simulation.what_if_engine import WhatIfEngine


def test_what_if_counterfactual_reasoning():
    engine = WhatIfEngine()

    # 1. What if MFA is disabled?
    res_mfa = engine.evaluate_what_if(
        target_twin_id="twn_test",
        question="What if MFA is disabled on all admin accounts?",
        hypothetical_changes={"disable_mfa": True},
    )
    assert res_mfa.simulated_risk_delta > +30.0
    assert res_mfa.simulated_blast_radius == "EXTENSIVE"
    assert res_mfa.is_simulation is True

    # 2. What if certificate is revoked?
    res_cert = engine.evaluate_what_if(
        target_twin_id="twn_test",
        question="What if edge SSL certificate is revoked?",
        hypothetical_changes={"revoke_certificate": True},
    )
    assert res_cert.simulated_risk_delta > 0.0
    assert len(res_cert.findings) >= 1
