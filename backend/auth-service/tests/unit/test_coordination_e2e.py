import pytest
from app.services.global_defense.global_defense_coordination_engine import GlobalDefenseCoordinationEngine

def test_complete_phase28_global_defense_coordination_e2e():
    engine = GlobalDefenseCoordinationEngine()
    
    # 1. Create Coordination Case
    case = engine.create_coordination_case(
        objective="Joint Mitigation of DarkStorm Lateral Movement",
        participating_entities=["tenant_finance_alpha", "tenant_cloud_beta"],
        classification="CONFIDENTIAL",
    )
    assert case.coordination_id is not None
    
    # 2. Evaluate Sharing Policy & Sanitize Payload
    pol = engine.policy_engine.evaluate_sharing("default_tenant", "tenant_finance_alpha", "CONFIDENTIAL", "THREAT_DEFENSE")
    assert pol["allowed"] is True
    
    san = engine.sanitization_engine.sanitize_payload({
        "indicator": "darkstorm.c2.net",
        "internal_ip": "10.0.8.22",
        "secret_token": "sk_live_secret",
    })
    assert san.sanitized_payload["internal_ip"] == "[REDACTED_PRIVATE_IP]"
    assert san.sanitized_payload["secret_token"] == "[REDACTED_SECRET]"
    
    # 3. Cross-Tenant Correlation
    corr = engine.correlation_guard.correlate_signals_privacy_preserving({
        "tenant_finance_alpha": ["darkstorm.c2.net"],
        "tenant_cloud_beta": ["darkstorm.c2.net"],
    })
    assert corr["shared_cross_tenant_intersections_count"] == 1
    
    # 4. Create Coordinated Response Plan
    plan = engine.response_engine.create_response_plan(
        coordination_id=case.coordination_id,
        objective="Synchronized WAF Rule Enforcement",
        participants=["tenant_finance_alpha", "tenant_cloud_beta"],
        actions=[{"step": 1, "action": "WAF Enforcement"}],
        approvals=["CISO", "SOC_LEAD"],
    )
    assert plan.plan_id is not None
    
    # 5. Four-Eyes Multi-Party Approval Gate
    gate1 = engine.approval_gate.approve_action(plan.plan_id, "SOC_LEAD")
    assert gate1["four_eyes_satisfied"] is False
    
    gate2 = engine.approval_gate.approve_action(plan.plan_id, "CISO")
    assert gate2["four_eyes_satisfied"] is True
    assert engine.approval_gate.verify_execution_authorization(plan.plan_id) is True
    
    # 6. Record Milestones & Evaluate SLA
    engine.timeline_engine.record_milestone(case.coordination_id, "APPROVED", "Four-Eyes Multi-Party Signed")
    sla = engine.sla_engine.evaluate_sla(case.coordination_id, notification_seconds=60, ack_seconds=120, response_seconds=600, recovery_seconds=1200)
    assert sla.is_compliant is True
    
    # 7. Publish Defensive Knowledge for Community Reuse
    dk = engine.knowledge_engine.publish_knowledge(
        problem="DarkStorm WAF bypass via encoded payload",
        evidence=["Regex evasion in HTTP URI"],
        defensive_technique="Deploy Normalized URI Decoding WAF rule",
        validation_result="100% containment in Digital Twin Sandbox",
        compatibility=["NGINX_INGRESS", "FASTAPI_GW"],
    )
    assert dk.knowledge_id is not None
    
    # 8. Scorecard Metrics
    sc = engine.scorecard_engine.evaluate_scorecard()
    assert sc.threat_readiness_score >= 0.90
