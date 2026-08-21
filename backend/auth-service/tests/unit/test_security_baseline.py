import pytest
from app.services.assurance.security_drift_engine import SecurityDriftEngine


def test_security_baseline_hashing():
    engine = SecurityDriftEngine()

    baseline = engine.establish_baseline(
        baseline_id="base_auth_prod",
        parameters={"mfa_required": True, "session_timeout_seconds": 900, "rate_limit_per_min": 100},
    )

    assert baseline.baseline_id == "base_auth_prod"
    assert len(baseline.configuration_hash) == 64  # SHA-256
