import pytest
from app.services.hunting.threat_hunting_fabric import ThreatHuntingFabric
from app.services.hunting.prediction_calibration_engine import PredictionCalibrationEngine


def test_autonomous_threat_hunting_e2e():
    fabric = ThreatHuntingFabric()
    calib = PredictionCalibrationEngine()

    # 1. Early warning triggers on weak signals
    warning = fabric.early_warning.evaluate_weak_signals(
        target_subject="auth.target-enterprise.com",
        signals=[
            {"type": "CERT_CHANGE", "title": "New certificate detected"},
            {"type": "TRUST_DROP", "title": "Trust score decreased"},
            {"type": "INFRA_CLUSTER", "title": "Shared IP subnet with known C2"},
        ],
    )
    assert warning is not None
    assert warning.warning_level in ("WATCH", "ELEVATED", "HIGH")

    # 2. Fabric generates hypothesis
    hyp = fabric.create_hunt_hypothesis(
        title="Hunt for Targeted Phishing Gateway & C2",
        description="Correlated weak signals indicate potential C2 staging",
        hypothesis_type="PHISHING_CAMPAIGN",
        target_assets=["auth.target-enterprise.com"],
        initial_evidence=[{"source": "EarlyWarning", "warning_id": warning.warning_id}],
    )

    # 3. Fabric runs bounded hunt
    result = fabric.run_bounded_hunt(hyp.hypothesis_id)
    assert result.result_id.startswith("res_")
    assert len(result.attack_paths) >= 1
    assert len(result.recommendations) >= 1

    # 4. Fabric issues predictive forecast
    prediction = fabric.predictive.forecast_threat_progression(
        target_subject="auth.target-enterprise.com",
        prediction_type="EXPOSURE_SPIKE",
        horizon="SHORT_TERM",
        predicted_probability=0.85,
    )

    # 5. Feedback calibration records outcome
    updated_pred = calib.record_prediction_outcome(prediction, "CORRECT")
    metrics = calib.calculate_calibration_metrics([updated_pred])
    assert metrics["resolved_count"] == 1
    assert metrics["accuracy"] == 1.0
