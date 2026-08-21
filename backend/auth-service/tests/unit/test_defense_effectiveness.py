import pytest
from app.services.adaptive_defense.defense_effectiveness_engine import DefenseEffectivenessEngine


def test_defense_effectiveness_scorecard():
    engine = DefenseEffectivenessEngine()
    eff = engine.calculate_effectiveness(
        tenant_id="tenant_eff",
        action_id="chg_001",
        threat_reduction=90.0,
        exposure_reduction=80.0,
        control_improvement=95.0,
        service_stability=99.0,
    )

    assert eff.overall_effectiveness > 85.0
    assert eff.residual_risk_score < 15.0
    assert eff.threat_reduction_score == 90.0
