import pytest
from app.services.predictive.threat_anomaly_engine import ThreatAnomalyEngine


def test_threat_anomaly_z_score_detection():
    engine = ThreatAnomalyEngine()
    engine.set_baseline("domain_creations_hourly", mean=10.0, std=2.0, tenant_id="tenant_anom")

    # Normal observation (12.0) -> No anomaly (z = 1.0 < 3.0)
    res_normal = engine.evaluate_metric("domain_creations_hourly", observed_value=12.0, z_threshold=3.0, tenant_id="tenant_anom")
    assert res_normal is None

    # Anomalous burst (25.0) -> z = 7.5 >= 3.0
    res_anom = engine.evaluate_metric("domain_creations_hourly", observed_value=25.0, z_threshold=3.0, tenant_id="tenant_anom")
    assert res_anom is not None
    assert res_anom.anomaly_type == "DOMAIN_CREATIONS_HOURLY_SPIKE"
    assert res_anom.z_score == 7.5
    assert res_anom.confidence >= 0.90
