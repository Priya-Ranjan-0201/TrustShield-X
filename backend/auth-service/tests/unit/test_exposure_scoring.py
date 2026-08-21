import pytest
from app.services.exposure.exposure_scoring_engine import ExposureScoringEngine
from app.schemas.exposure_models import AssetDTO, AssetBaselineDTO


def test_exposure_score_calculation():
    asset = AssetDTO(
        asset_id="ast_301",
        asset_type="DOMAIN",
        canonical_identifier="vpn-gw.example.com",
        display_identifier="vpn-gw.example.com",
        criticality="CRITICAL",
    )
    baseline = AssetBaselineDTO(
        baseline_id="base_301",
        asset_id="ast_301",
        exposed_ports=[443],
    )

    # Observation with public reachability, 3 open ports including SSH (22), and campaign linkage
    obs = {
        "is_public_facing": True,
        "exposed_ports": [80, 443, 22],
    }

    res = ExposureScoringEngine.calculate_exposure_score(
        asset=asset,
        baseline=baseline,
        current_observation=obs,
        has_active_campaign_link=True,
    )

    # Base: 20 + 15 (public) + 15 (ports) + 20 (high-risk SSH) + 20 (campaign) = 90
    # Multiplier: 1.6 (CRITICAL) -> min(100.0, 90 * 1.6) = 100.0
    assert res["exposure_score"] >= 90.0
    assert len(res["contributing_factors"]) >= 3
