import pytest
from app.services.digital_twin_lab.cyber_defense_digital_twin_engine import CyberDefenseDigitalTwinEngine

def test_complete_phase26_digital_twin_e2e_lifecycle():
    engine = CyberDefenseDigitalTwinEngine()
    
    # 1. Check Twin State & Freshness
    overview = engine.get_digital_twin_overview("default_tenant")
    assert overview["twin_freshness_status"] == "FRESH"
    
    # 2. Select & Run Scenario
    scen = engine.scenario_engine.get_scenario("scen_phishing_lateral_movement")
    assert scen is not None
    
    # 3. Simulate Attack Path
    sim = engine.attack_path_engine.simulate_attack_path(scen.scenario_id)
    assert len(sim.stages) >= 3
    
    # 4. Evaluate Defense Path
    defense_res = engine.defense_path_engine.evaluate_defense_interception(sim.potential_attack_paths[0], ["ctl_waf_gateway"])
    assert defense_res["is_contained"] is True
    
    # 5. Evaluate Business Impact
    impact = engine.impact_engine.simulate_business_impact(scen.scenario_id)
    assert impact.financial_impact_status == "FINANCIAL_IMPACT_NOT_MODELED"
    
    # 6. Compare Strategies (Pareto)
    strat_res = engine.strategy_optimizer.compare_strategies(scen.scenario_id)
    assert strat_res.recommended_strategy == "STRATEGY_A_AUTOMATED_ISOLATION"
    
    # 7. Record Calibration vs Real Drill
    calib = engine.calibration_engine.record_calibration(
        scenario_id=scen.scenario_id,
        predicted_outcome={"containment_time_seconds": 45.0},
        actual_outcome={"containment_time_seconds": 42.0},
    )
    assert calib.error_classification == "CORRECT"
    
    # 8. Log Audit Chain
    audit_hash = engine.governance_engine.log_simulation_audit("E2E_SIMULATION_CYCLE_COMPLETED", {"scenario_id": scen.scenario_id})
    assert len(audit_hash) == 64
