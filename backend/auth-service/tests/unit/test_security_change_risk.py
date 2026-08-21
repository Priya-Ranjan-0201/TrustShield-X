import pytest
from app.services.assurance.security_assurance_score_engine import SecurityAssuranceScoreEngine
from app.schemas.assurance_models import SecurityControlRegistryDTO


def test_security_change_risk_evaluation():
    engine = SecurityAssuranceScoreEngine()

    controls = [
        SecurityControlRegistryDTO(control_id="c1", name="C1", category="PREVENTIVE", description="D", verification_state="VERIFIED"),
        SecurityControlRegistryDTO(control_id="c2", name="C2", category="ACCESS_CONTROL", description="D", verification_state="DEGRADED"),
    ]

    # Degraded controls lower the overall score
    summary = engine.calculate_summary(controls)
    assert summary.overall_assurance_score < 100.0
    assert summary.controls_degraded == 1
