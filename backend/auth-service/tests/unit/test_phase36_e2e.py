import pytest
from app.services.cyber_crisis_command import (
    cyber_crisis_command_engine,
    crisis_escalation_engine,
    crisis_communication_engine,
    crisis_decision_engine,
    crisis_recovery_engine,
    truthshield_security_copilot
)

def test_phase36_full_operational_loop_e2e():
    tenant = "tenant-e2e-p36"
    
    # 1. DETECT & DECLARE
    crisis = cyber_crisis_command_engine.declare_crisis("CRISIS-E2E", tenant, ["INC-88"], "CISO", "Full E2E Crisis", severity="SEV_1")
    assert crisis["lifecycle_state"] == "CRISIS_DECLARED"
    
    # 2. COMMAND & SITUATIONAL AWARENESS
    cyber_crisis_command_engine.assign_role("CRISIS-E2E", tenant, "SECURITY_LEAD", "secops@truthshield.io", "CISO")
    sit = cyber_crisis_command_engine.generate_situational_awareness("CRISIS-E2E", tenant)
    assert sit["crisis_risk"]["composite_risk_score"] > 0
    
    # 3. ESCALATION & SLA
    esc = crisis_escalation_engine.evaluate_escalation_triggers("CRISIS-E2E", tenant, "SEV_1", 30, 4, 1)
    assert esc["escalated"] is True
    
    # 4. DECISION INTELLIGENCE
    opts = crisis_decision_engine.analyze_response_options("CRISIS-E2E", tenant, "API-GW", "Ransomware")
    dec = crisis_decision_engine.record_decision("DEC-E2E-1", "CRISIS-E2E", tenant, "Select response", opts, "OPT-A", "CISO", "Pareto optimal")
    assert dec["selected_option_id"] == "OPT-A"
    
    # 5. COMMUNICATIONS WITH FACT GOVERNANCE
    comm = crisis_communication_engine.create_communication_draft(
        "COMM-E2E", "CRISIS-E2E", tenant, "INTERNAL_SECURITY", "SOC Team",
        confirmed_facts=["Option A executed", "Boundary secure"],
        suspected_facts=["APT29 involvement"],
        unknowns=["Initial compromised credential"],
        draft_content="Internal operational report"
    )
    assert comm["status"] == "DRAFT"
    
    # 6. COPILOT DECISION SUPPORT
    copilot_res = truthshield_security_copilot.query_copilot("What is confirmed?", tenant, "user-ciso", mode="CRISIS_COMMANDER")
    assert copilot_res["confidence"] == "HIGH_CONFIDENCE"
    
    # 7. RECOVERY & INDEPENDENT VERIFICATION
    rec_task = crisis_recovery_engine.create_recovery_task("REC-E2E-1", "CRISIS-E2E", tenant, "Node 01 Restore", "APPLICATION", "DevOps")
    assert rec_task["status"] == "NOT_STARTED"
    
    ver = crisis_recovery_engine.verify_recovery("CRISIS-E2E", tenant, {"security_probe_success": True})
    assert ver["overall_recovery_status"] == "RECOVERY_VERIFIED"
    
    # 8. LESSONS LEARNED & CLOSURE
    lessons = crisis_recovery_engine.generate_candidate_lessons_learned("CRISIS-E2E", tenant, [])
    assert len(lessons) >= 2
    
    closed = cyber_crisis_command_engine.transition_lifecycle_state("CRISIS-E2E", tenant, "CLOSED", "CISO", "Crisis successfully mitigated and verified")
    assert closed["is_closed"] is True
