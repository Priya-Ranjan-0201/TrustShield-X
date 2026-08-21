import pytest
from app.services.adaptive_defense.exposure_control_engine import ExposureControlEngine


def test_attack_surface_multidimensional_scorecard():
    engine = ExposureControlEngine()

    score = engine.calculate_attack_surface(
        tenant_id="tenant_corp",
        exposed_assets=5,
        exposed_services=3,
        unpatched_vulnerabilities=2,
        identity_risks=1,
        third_party_deps=5,
        cloud_assets=8,
        control_coverage_pct=90.0,
    )

    assert score.exposed_assets_score == 20.0
    assert score.vulnerabilities_score == 24.0
    assert score.control_coverage_score == 90.0
    assert 0.0 <= score.overall_attack_surface_score <= 100.0
