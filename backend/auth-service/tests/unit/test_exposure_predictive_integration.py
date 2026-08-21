import pytest
from app.services.exposure.asset_inventory_service import AssetInventoryService
from app.services.predictive.predictive_risk_engine import PredictiveRiskEngine


def test_exposure_predictive_risk_projection():
    inventory = AssetInventoryService()
    pred_engine = PredictiveRiskEngine()

    asset = inventory.register_asset(
        asset_type="DOMAIN",
        raw_identifier="gateway.truthshield.io",
        criticality="HIGH",
        tenant_id="tenant_pred",
    )

    # Predict risk trajectory over 24h horizon with accelerating campaign velocity
    pred_risk = pred_engine.calculate_predictive_risk(
        entity_or_campaign_id=asset.canonical_identifier,
        current_observed_risk=asset.risk_score,
        campaign_velocity=1.85,
        anomaly_z_score=4.5,
        source_reliability=0.95,
        time_horizon="24H",
    )

    assert pred_risk.projected_risk > asset.risk_score
    assert pred_risk.risk_delta > 0.0
    assert pred_risk.prediction_confidence >= 0.80
