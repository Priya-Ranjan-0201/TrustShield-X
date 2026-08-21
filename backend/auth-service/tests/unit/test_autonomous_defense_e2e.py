import pytest
from app.services.autonomous_defense_orchestrator import AutonomousDefenseOrchestrator
from app.schemas.autonomous_defense_models import DecisionContextDTO


def test_full_autonomous_defense_core_loop():
    """
    E2E Test of the Full Autonomous Cyber Defense Core Loop:
    DETECT → CORRELATE → UNDERSTAND → ASSESS RISK → DECIDE → AUTHORIZE → SIMULATE → EXECUTE → VERIFY → AUDIT → LEARN
    """
    orch = AutonomousDefenseOrchestrator()

    # 1. DETECT & CORRELATE (Ingest threat contexts)
    ctx1 = DecisionContextDTO(
        incident_id="INC-2026-9001",
        risk_score=92.0,
        severity="CRITICAL",
        confidence=0.96,
        action_type="BLOCK_DOMAIN",
        target="phishing-c2-server.org",
        evidence_ids=["EVID_APK_DEX_01", "EVID_NETWORK_PCAP_09"],
    )
    ctx2 = DecisionContextDTO(
        incident_id="INC-2026-9001",
        risk_score=88.0,
        severity="HIGH",
        confidence=0.94,
        action_type="FREEZE_UPI_HANDLE",
        target="fraud.collect@upi",
        evidence_ids=["EVID_UPI_TELEMETRY_44"],
    )

    # 2. DECIDE & CREATE RESPONSE PLAN
    plan = orch.create_response_plan(
        tenant_id="tenant_e2e",
        incident_id="INC-2026-9001",
        title="E2E Multi-Vector Containment Plan",
        description="Coordinated C2 domain block and fraud handle freeze",
        threat_contexts=[ctx1, ctx2],
    )
    assert plan.state == "CREATED"
    assert len(plan.actions) == 2
    assert plan.requires_human_approval is True

    # 3. SIMULATE (Zero external mutation dry-run)
    sim = orch.simulate_plan(plan.plan_id, "tenant_e2e")
    assert sim.policy_evaluation_passed is True
    assert sim.mutations_expected == 0
    assert plan.state == "SIMULATED"

    # 4. AUTHORIZE (Four-Eyes approval for each high-impact action)
    for act in plan.actions:
        appr_id = orch.request_action_approval(
            plan_id=plan.plan_id,
            action_id=act.action_id,
            requested_by="analyst_priya",
            reason="Confirmed high confidence threat indicators",
            tenant_id="tenant_e2e",
        )
        orch.approve_action(
            approval_id=appr_id,
            approver_id="soc_lead_arjun",
            decision="APPROVED",
            decision_reason="Verified by senior SOC lead",
            tenant_id="tenant_e2e",
        )

    assert plan.all_approved is True
    assert plan.state == "APPROVED"

    # 5. EXECUTE (Safe adapter execution)
    executed_actions = orch.execute_plan(plan.plan_id, "tenant_e2e")
    assert len(executed_actions) == 2
    assert all(a.state == "EXECUTED" for a in executed_actions)
    assert plan.state == "EXECUTED"

    # 6. VERIFY (Post-action empirical state probe)
    verifications = orch.verify_plan(plan.plan_id, "tenant_e2e")
    assert len(verifications) == 2
    assert all(v.verification_passed for v in verifications)
    assert plan.state == "VERIFIED"

    # 7. LEARN & EFFECTIVENESS SCORING
    effectiveness = orch.effectiveness_engine.calculate_effectiveness(
        plan=plan,
        verifications=verifications,
        initial_risk=92.0,
        residual_risk=8.5,
        time_to_containment_seconds=3.8,
    )
    assert effectiveness.effectiveness_score >= 90.0
    assert effectiveness.containment_success_rate == 1.0

    # 8. AUDIT (Tamper-evident SHA-256 chained log)
    audit_trail = orch.get_audit_trail()
    assert len(audit_trail) >= 6
    # Verify cryptographic hash chaining
    for i in range(1, len(audit_trail)):
        assert audit_trail[i]["previous_hash"] == audit_trail[i - 1]["current_hash"]
