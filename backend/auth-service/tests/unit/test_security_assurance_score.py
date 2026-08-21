import pytest
from app.services.assurance.security_assurance_score_engine import SecurityAssuranceScoreEngine
from app.schemas.assurance_models import SecurityControlRegistryDTO


def test_security_assurance_score_calculation():
    engine = SecurityAssuranceScoreEngine()

    controls = [
        SecurityControlRegistryDTO(control_id="c1", name="C1", category="PREVENTIVE", description="D", verification_state="VERIFIED"),
        SecurityControlRegistryDTO(control_id="c2", name="C2", category="ACCESS_CONTROL", description="D", verification_state="VERIFIED"),
        SecurityControlRegistryDTO(control_id="c3", name="C3", category="AUDIT", description="D", verification_state="VERIFIED"),
    ]

    summary = engine.calculate_summary(controls)
    assert summary.overall_assurance_score == 100.0
    assert summary.control_coverage_percentage == 100.0

    # Test penalty with active drift
    summary_with_drift = engine.calculate_summary(controls, active_drifts_count=2)
    assert summary_with_drift.overall_assurance_score == 90.0
