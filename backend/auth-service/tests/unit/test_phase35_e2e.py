import pytest
from app.services.cyber_digital_twin import (
    cyber_digital_twin_engine,
    cyber_simulation_scenario_engine,
    attack_simulation_engine,
    attack_path_prediction_engine,
    what_if_simulation_engine,
    defense_optimization_engine,
    autonomous_defense_engine,
    action_verification_rollback_engine,
    incident_replay_purple_team_engine,
    digital_twin_validation_governance_engine
)

def test_phase35_full_closed_loop_e2e():
    tenant = "tenant-e2e-p35"
    
    # 1. OBSERVE & MODEL: Digital Twin Environment & Snapshot
    env = cyber_digital_twin_engine.create_environment("ENV-E2E", tenant, "PRODUCTION_REPLICA", initial_state={"assets": [{"id": "API-GW", "type": "INGRESS"}]})
    snap = cyber_digital_twin_engine.create_snapshot("SNAP-E2E-1", "ENV-E2E", tenant)
    assert snap["is_immutable"] is True
    
    # 2. SIMULATE: Attack Simulation
    scen = cyber_simulation_scenario_engine.create_scenario("SCEN-E2E", tenant, "Ransomware Ingress", "Test", "Containment", "ATTACK_SIMULATION")
    atk = attack_simulation_engine.run_attack_simulation("ATK-E2E", tenant, "API-GW", "LOCKBIT_RANSOMWARE")
    assert atk["contained"] is True
    
    # 3. PREDICT: Predicted Attack Path
    pred = attack_path_prediction_engine.predict_attack_paths("PRED-E2E", tenant, "API-GW", "CORE-VAULT")
    assert pred["status"] == "PREDICTED_ATTACK_PATH"
    
    # 4. OPTIMIZE: What-If & Defense Optimization
    whatif = what_if_simulation_engine.run_what_if("WIF-E2E", tenant, "API-GW", "PATCH_VULNERABILITY")
    assert whatif["risk_change"] == -4.5
    
    opt = defense_optimization_engine.optimize_defense_strategy("OPT-E2E", tenant, "API-GW", "Ransomware")
    assert opt["recommended_strategy"]["is_pareto_optimal"] is True
    
    # 5. APPROVE & EXECUTE: Autonomous Action with Governance
    autonomous_defense_engine.set_tenant_autonomy_level(tenant, "LEVEL_2")
    act = autonomous_defense_engine.propose_defensive_action("ACT-E2E", tenant, "API-GW", "QUARANTINE_NON_CRITICAL_ENDPOINT")
    assert act["approval_requirement"] == "HUMAN_APPROVAL_REQUIRED"
    
    app = autonomous_defense_engine.record_approval("ACT-E2E", tenant, "SECOPS-LEAD")
    assert app["status"] == "APPROVED"
    
    executed = autonomous_defense_engine.execute_action("ACT-E2E", tenant)
    assert executed["status"] == "EXECUTED"
    
    # 6. VERIFY: Independent Telemetry Verification
    ver = action_verification_rollback_engine.verify_action_execution("VER-E2E", "ACT-E2E", tenant, {"independent_probe_success": True})
    assert ver["status"] == "VERIFIED"
    
    # 7. AUDIT: SHA-256 Chained Audit Event
    audit = digital_twin_validation_governance_engine.record_audit_event("EV-E2E", tenant, "AUTONOMOUS_ACTION_VERIFIED", {"action_id": "ACT-E2E"})
    assert audit["current_hash"] is not None
