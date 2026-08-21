import pytest
from app.services.global_intelligence.global_threat_intelligence_fusion_engine import GlobalThreatIntelligenceFusionEngine

def test_complete_phase27_threat_intelligence_e2e_lifecycle():
    engine = GlobalThreatIntelligenceFusionEngine()
    
    # 1. Ingest & Normalize
    rec = engine.ingest_record("src_global_exchange", {"indicator": "c2.darkstorm.internal", "severity": "HIGH", "confidence": 0.95})
    assert rec.indicator == "c2.darkstorm.internal"
    
    # 2. Correlate Campaign
    cmp_obj = engine.campaign_engine.get_campaign("cmp_darkstorm_2026")
    assert cmp_obj is not None
    assert cmp_obj.evolution_status == "EXPANDING"
    
    # 3. Detect Emerging Threat & Velocity
    vel = engine.velocity_engine.calculate_velocity(cmp_obj.campaign_id, new_indicators_24h=30, baseline_indicators_daily=5)
    assert vel["velocity_surge_detected"] is True
    
    # 4. Trigger Early Warning
    warn = engine.early_warning_engine.trigger_warning(cmp_obj.name, "HIGH", velocity_score=0.85, affected_assets=["ast_api_gw"])
    assert warn.severity == "HIGH"
    
    # 5. Evaluate Exposure
    exp = engine.exposure_engine.evaluate_exposure(cmp_obj.campaign_id, ["ast_api_gw", "ast_auth_cluster"])
    assert exp["exposure_score"] >= 0.80
    
    # 6. Generate Predictive Forecast
    fcst = engine.forecasting_engine.generate_forecast(
        subject="DarkStorm Lateral Expansion",
        horizon="SHORT_TERM",
        prediction="35% surge in token stuffing over 72h.",
        evidence=["NetFlow surge", "ASN clustering"],
    )
    assert fcst.calibration_status == "CALIBRATED"
    
    # 7. Generate Defensive Hypothesis for Digital Twin
    hyp = engine.hypothesis_engine.generate_hypothesis(
        threat_id=cmp_obj.campaign_id,
        statement="Enforcing rate limiting blocks 85% of DarkStorm initial access.",
        testable_criteria="Simulated containment latency < 30s",
    )
    assert hyp.digital_twin_scenario_id == "scen_phishing_lateral_movement"
    
    # 8. Check Overview
    overview = engine.get_global_intelligence_overview()
    assert overview["feed_health_status"] == "HEALTHY"
