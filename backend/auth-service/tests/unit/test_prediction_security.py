import pytest
from app.services.predictive.early_warning_engine import EarlyWarningEngine
from app.services.predictive.threat_hunting_engine import ThreatHuntingEngine


def test_isolated_prediction_cannot_trigger_destructive_response():
    # Invariant: Predictive intelligence provides warnings only; never executes destructive response
    engine = EarlyWarningEngine()
    warning = engine.evaluate_weak_signals(
        affected_entities=["domain:c2-phish.net"],
        indicator_count=4,
        reused_infrastructure_count=2,
        cross_modal_convergence=True,
    )
    assert warning is not None
    # Verify warning contains only advisory projected risk, no direct response execution fields
    assert hasattr(warning, "projected_risk_score")
    assert not hasattr(warning, "executed_action")


def test_threat_hunt_query_bounds_and_safety():
    engine = ThreatHuntingEngine()
    # Invariant: Query limits max_depth to prevent graph traversal recursion denial of service
    query = engine.translate_natural_language_query("Find everything connected recursively forever", "tenant_sec")
    assert query.max_depth <= 5
