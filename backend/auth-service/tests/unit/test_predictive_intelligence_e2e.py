import pytest
from app.services.predictive.threat_signal_normalization_service import ThreatSignalNormalizationService
from app.services.predictive.threat_feed_quality_engine import ThreatFeedQualityEngine
from app.services.predictive.threat_anomaly_engine import ThreatAnomalyEngine
from app.services.predictive.early_warning_engine import EarlyWarningEngine
from app.services.predictive.campaign_forecasting_engine import CampaignForecastingEngine
from app.services.predictive.predictive_risk_engine import PredictiveRiskEngine
from app.services.predictive.threat_hunting_engine import ThreatHuntingEngine
from app.services.predictive.prediction_calibration_engine import PredictionCalibrationEngine


def test_full_predictive_intelligence_core_loop():
    """
    E2E Test of the Full Predictive Threat Intelligence Core Loop:
    PREDICT → HUNT → CORRELATE → PRIORITIZE → WARN → VALIDATE → LEARN
    """
    # 1. INGEST & NORMALIZE SIGNALS
    sig_service = ThreatSignalNormalizationService()
    sig1 = sig_service.ingest_signal(
        signal_type="DOMAIN",
        source="src_commercial_threat_feed",
        entity_id="fake-payment-portal-bank.com",
        confidence=0.90,
        severity="HIGH",
        tenant_scope="tenant_e2e",
    )
    assert sig1.lifecycle_state == "FIRST_SEEN"

    # 2. SOURCE QUALITY WEIGHTING
    feed_quality = ThreatFeedQualityEngine()
    weighted_conf = feed_quality.weight_signal_confidence(sig1.source, sig1.confidence)
    assert weighted_conf >= 0.70

    # 3. ANOMALY DETECTION
    anomaly_engine = ThreatAnomalyEngine()
    anomaly_engine.set_baseline("phishing_burst", mean=5.0, std=1.0, tenant_id="tenant_e2e")
    anomaly = anomaly_engine.evaluate_metric("phishing_burst", observed_value=15.0, z_threshold=3.0, tenant_id="tenant_e2e")
    assert anomaly is not None
    assert anomaly.z_score == 10.0

    # 4. EARLY WARNING GENERATION
    warning_engine = EarlyWarningEngine()
    warning = warning_engine.evaluate_weak_signals(
        affected_entities=["fake-payment-portal-bank.com", "apk:sha256_dropper_e2e"],
        indicator_count=3,
        reused_infrastructure_count=2,
        cross_modal_convergence=True,
        tenant_id="tenant_e2e",
    )
    assert warning is not None
    assert warning.severity == "HIGH"

    # 5. CAMPAIGN EXPANSION FORECAST
    forecast_engine = CampaignForecastingEngine()
    forecast = forecast_engine.forecast_campaign(
        campaign_id="CAMP-2026-0891",
        entity_count=6,
        daily_growth_rate=1.80,
        current_risk=70.0,
    )
    assert forecast.growth_state == "ACCELERATING"
    assert forecast.projected_risk > 70.0

    # 6. PREDICTIVE RISK ESTIMATION
    risk_engine = PredictiveRiskEngine()
    pred_risk = risk_engine.calculate_predictive_risk(
        entity_or_campaign_id="CAMP-2026-0891",
        current_observed_risk=70.0,
        campaign_velocity=1.80,
        anomaly_z_score=anomaly.z_score,
        source_reliability=0.90,
    )
    assert pred_risk.projected_risk > 70.0

    # 7. THREAT HUNTING
    hunt_engine = ThreatHuntingEngine()
    hunt_engine.seed_hunt_entity("tenant_e2e", {
        "value": "fake-payment-portal-bank.com",
        "campaign_id": "CAMP-2026-0891",
    })
    hunt_query = hunt_engine.translate_natural_language_query("Find campaigns related to fake-payment-portal-bank.com", "tenant_e2e")
    hunt_res = hunt_engine.execute_hunt(hunt_query)
    assert hunt_res.total_matched == 1

    # 8. CALIBRATION & LEARNING
    cal_engine = PredictionCalibrationEngine()
    pred = cal_engine.record_prediction(
        prediction_text="CAMP-2026-0891 will register sibling C2 domain within 48h",
        predicted_probability=0.88,
    )
    outcome = cal_engine.evaluate_outcome(pred.prediction_id, "OCCURRED")
    assert outcome.actual_outcome == "OCCURRED"
    assert outcome.brier_score_contribution is not None
    assert outcome.brier_score_contribution < 0.05
