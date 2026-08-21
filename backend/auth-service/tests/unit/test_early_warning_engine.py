import pytest
from app.services.predictive.early_warning_engine import EarlyWarningEngine


def test_early_warning_multi_signal_detection():
    engine = EarlyWarningEngine()
    # Multi-signal cross-modal convergence
    warning = engine.evaluate_weak_signals(
        affected_entities=["domain:c2-phish.net", "apk:sha256_dropper"],
        indicator_count=4,
        reused_infrastructure_count=2,
        certificate_reuse=True,
        cross_modal_convergence=True,
        tenant_id="tenant_ew",
    )
    assert warning is not None
    assert warning.warning_type == "CROSS_MODAL_THREAT_CONVERGENCE"
    assert warning.confidence == "HIGH"
    assert warning.propagation_score > 0.50
    assert warning.projected_risk_score > warning.current_risk_score


def test_early_warning_single_weak_signal_suppressed():
    engine = EarlyWarningEngine()
    # Single indicator with no reused infrastructure or certificate overlap
    warning = engine.evaluate_weak_signals(
        affected_entities=["domain:single-domain.net"],
        indicator_count=1,
        reused_infrastructure_count=0,
        certificate_reuse=False,
        cross_modal_convergence=False,
        tenant_id="tenant_ew",
    )
    # Invariant: A single isolated weak signal must NOT trigger high-confidence alert
    assert warning is None
