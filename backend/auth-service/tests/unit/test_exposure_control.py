import pytest
from app.services.adaptive_defense.exposure_control_engine import ExposureControlEngine


def test_exposure_control_mitigation_coverage():
    engine = ExposureControlEngine()

    # High coverage (95%) reduces overall score
    score_high_cov = engine.calculate_attack_surface(
        tenant_id="tenant_secured",
        exposed_assets=10,
        unpatched_vulnerabilities=4,
        control_coverage_pct=95.0,
    )

    # Low coverage (30%) increases overall score
    score_low_cov = engine.calculate_attack_surface(
        tenant_id="tenant_unsecured",
        exposed_assets=10,
        unpatched_vulnerabilities=4,
        control_coverage_pct=30.0,
    )

    assert score_high_cov.overall_attack_surface_score < score_low_cov.overall_attack_surface_score
