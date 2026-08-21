import pytest
from app.services.autonomous_defense.autonomous_soc_engine import AutonomousSOCEngine

def test_autonomous_defense_complete_closed_loop_e2e():
    engine = AutonomousSOCEngine()
    
    # 1. OBSERVE & DETECT -> Rule Evaluation
    rules = engine.detection_engine.list_rules()
    assert len(rules) >= 1
    
    # 2. HYPOTHESIZE & SIMULATE -> Digital Twin Sandbox
    sim = engine.digital_twin_bridge.simulate_candidate_improvement("Candidate Ingress WAF Rate-Limit")
    assert sim["simulation_status"] == "SIMULATED"
    
    # 3. RECOMMEND & EXPLAIN -> Decision Engine
    dec = engine.decision_engine.create_decision(
        decision_type="RESPONSE_RECOMMENDATION",
        recommendation="Apply Ingress WAF Rate-Limiting",
        evidence=["Phase 27 Early Warning", "Phase 26 Digital Twin Sandbox Log"],
        confidence=0.94,
        selected_action="WAF_RATE_LIMIT",
        expected_outcome="90% reduction in C2 attack traffic",
        rollback_plan="Revert WAF rate-limit ruleset",
        autonomy_level="LEVEL_4",
    )
    assert dec.decision_id is not None
    
    # 4. GOVERNANCE & APPROVE -> Autonomy Governance Engine (Level 4 Gate)
    gov_check = engine.autonomy_engine.validate_action_execution(
        current_autonomy="LEVEL_4",
        action_name=dec.selected_action,
        is_high_impact=True,
        has_approval=True,
    )
    assert gov_check["allowed"] is True
    
    # 5. RESPOND & MEASURE -> Response Optimization Engine
    rsp = engine.response_engine.evaluate_response_outcome(
        response_id="rsp_e2e_01",
        playbook_name="DarkStorm Mitigation",
        containment_time_sec=42.0,
        recovery_time_sec=110.0,
        has_collateral_impact=False,
    )
    assert rsp.effectiveness == "RESPONSE_EFFECTIVE"
    
    # 6. VERIFY -> Action Verification Engine
    ver = engine.verification_engine.verify_action(
        action_id="act_e2e_01",
        target="ast_api_gw",
        intended_outcome="WAF Rate-Limiting Active",
        observed_outcome="WAF Rate-Limiting Active; 0 collateral drop",
        telemetry_matches=True,
    )
    assert ver.is_verified is True
    
    # 7. LEARN & STORE -> Defensive Learning & Memory Engine
    learn_res = engine.learning_engine.evaluate_learning_candidate(
        observation="DarkStorm C2 Lateral Burst",
        evidence=dec.evidence,
        action_taken=dec.selected_action,
        expected_outcome=dec.expected_outcome,
        actual_outcome=ver.observed_outcome,
        is_verified_by_telemetry=True,
        confidence=0.95,
        applicability="TENANT_SPECIFIC",
    )
    assert learn_res["status"] == "LEARNED"
    
    stored_lesson = engine.memory_engine.store_lesson(learn_res["lesson"])
    assert stored_lesson.lesson_id is not None
    
    # 8. REVALIDATE & SCORECARD
    card = engine.get_autonomous_defense_scorecard()
    assert card.autonomy_level == "LEVEL_4"
    assert card.system_health == "HEALTHY"
