import pytest
from app.services.soc.security_operations_orchestrator import SecurityOperationsOrchestrator


def test_closed_loop_soc_operational_e2e_lifecycle():
    orch = SecurityOperationsOrchestrator()
    tenant = "tenant_e2e_soc"

    # 1. DETECT & ENRICH: Ingest normalized alert
    alert = orch.ingest_alert(
        tenant_id=tenant,
        source="EDR_DEFENDER",
        asset="srv_payment_gateway",
        severity="CRITICAL",
        confidence=0.96,
        evidence=["ev_pcap_88", "ev_sig_99"],
        indicator="198.51.100.42",
    )
    assert alert.alert_id is not None

    # 2. CORRELATE & CLUSTER: Group with related indicators
    clusters = orch.correlate_and_cluster(tenant)
    assert len(clusters) >= 1

    # 3. TRIAGE & PRIORITY: Compute explainable priority
    priority = orch.priority_engine.compute_priority(alert, asset_criticality=95.0, exposure_score=85.0)
    assert priority.priority_score > 75.0

    # 4. INVESTIGATE & BLAST RADIUS: Map observed vs potential assets
    deps = {"srv_payment_gateway": ["db_primary_vault", "srv_order_worker"]}
    blast_radius = orch.blast_radius_engine.evaluate_blast_radius("inc_e2e_01", ["srv_payment_gateway"], deps)
    assert "db_primary_vault" in blast_radius.potential_impact_assets

    # 5. INCIDENT LIFECYCLE: Advance state NEW -> TRIAGED -> INVESTIGATING -> CONTAINMENT_PENDING
    sm = orch.state_machine
    sm.init_incident("inc_e2e_01")
    sm.transition("inc_e2e_01", "TRIAGED")
    sm.transition("inc_e2e_01", "INVESTIGATING")
    sm.transition("inc_e2e_01", "CONTAINMENT_PENDING")

    # 6. INCIDENT COMMAND: Assign roles
    cmd = orch.command_engine.assign_command_team(
        incident_id="inc_e2e_01",
        commander="usr_ciso_alice",
        technical_lead="usr_eng_bob",
        comms_lead="usr_comms_carol",
        recovery_lead="usr_sre_dave",
        security_analyst="usr_analyst_eve",
    )
    assert cmd.incident_commander == "usr_ciso_alice"

    # 7. RESPONSE PLAN & SIMULATION: Generate dry-run response plan
    plan = orch.plan_generator.generate_plan("inc_e2e_01", "srv_payment_gateway", "CVE-2026-9942_RCE")
    assert plan.is_safe is True
    assert len(plan.rollback_steps) >= 1

    # 8. AUTHORIZATION, EXECUTION & EMPIRICAL VERIFICATION (Four-Eyes: Requester != Approver)
    action, ver = orch.execute_and_verify_action(
        incident_id="inc_e2e_01",
        target="srv_payment_gateway",
        provider="FIREWALL_DROP",
        requester_id="usr_analyst_eve",
        approver_id="usr_ciso_alice",
        tenant_id=tenant,
    )
    assert action.action_state == "EXECUTED"
    assert ver.verification_status == "VERIFIED_SUCCESS"
    assert ver.divergence_detected is False

    # 9. ADVANCE TO CONTAINED -> ERADICATION -> RECOVERY -> VALIDATION -> CLOSED
    sm.transition("inc_e2e_01", "CONTAINED")
    sm.transition("inc_e2e_01", "ERADICATION")
    sm.transition("inc_e2e_01", "RECOVERY")
    sm.transition("inc_e2e_01", "VALIDATION")
    sm.transition("inc_e2e_01", "CLOSED")

    # 10. POST-INCIDENT CLOSED-LOOP LEARNING
    lessons = orch.learning_engine.extract_lessons(
        incident_id="inc_e2e_01",
        expected_state="NETWORK_ISOLATION_APPLIED",
        actual_state="NETWORK_ISOLATION_APPLIED",
        mttd_minutes=4.2,
    )
    assert lessons["divergence_from_expected"] is False

    # 11. SOC SCORECARD
    scorecard = orch.scorecard_engine.compute_scorecard(tenant)
    assert scorecard.sla_compliance_pct > 95.0
    assert scorecard.scorecard_grade == "EXCELLENT"
