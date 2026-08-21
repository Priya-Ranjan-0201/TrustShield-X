import pytest
from app.services.mission_control_os.global_security_mission_control_engine import GlobalSecurityMissionControlEngine

def test_complete_phase29_mission_control_operating_system_e2e():
    engine = GlobalSecurityMissionControlEngine()
    
    # 1. Publish Event into Event Fabric
    evt_res = engine.event_fabric.publish_event(
        event_type="EARLY_WARNING",
        source="global_threat_intel",
        payload={"threat": "DarkStorm Surge", "velocity": 0.88},
        idempotency_key="idem_e2e_001",
    )
    assert evt_res["status"] == "PUBLISHED"
    
    # 2. Evaluate Priority
    prio = engine.priority_engine.evaluate_priority(severity_score=0.90, exposure_score=0.85, has_active_exploitation=True)
    assert prio["priority"] == "CRITICAL"
    
    # 3. Create & Route Mission Task
    task = engine.task_engine.create_task(
        title="Execute Four-Eyes WAF Mitigation",
        task_type="CONTAIN",
        owner="SOC_ANALYST_LEAD",
        priority=prio["priority"],
    )
    assert task.task_id is not None
    
    # 4. Check Blockers & Verify SLA
    diag = engine.blocker_engine.diagnose_blockers(task.task_id, missing_approvals=[], dependency_statuses={"soar": "HEALTHY"})
    assert diag["has_blockers"] is False
    
    sla = engine.sla_engine.evaluate_task_sla(task.task_id, allocated_sla_seconds=1800, elapsed_seconds=300)
    assert sla["is_compliant"] is True
    
    # 5. Run Cross-Subsystem Mission Workflow
    wf = engine.workflow_orchestrator.run_workflow(
        name="THREAT_TO_INVESTIGATION",
        trigger_event="EARLY_WARNING",
        steps=[{"step": 1, "action": "WAF_RATE_LIMIT"}],
    )
    assert wf.status == "RUNNING"
    
    # 6. Query Subsystem Context
    ctx = engine.integration_bridge.query_cross_subsystem_context()
    assert ctx["integration_verified"] is True
    
    # 7. Ask Copilot Query with Evidence Grounding
    copilot_ans = engine.copilot_bridge.answer_operational_query("What is happening right now?")
    assert copilot_ans["claim_status"] == "OBSERVED"
    
    # 8. Check Health & Mission Overview
    ov = engine.get_mission_overview()
    assert ov["operational_status"] == "OPERATIONAL"
    assert ov["system_health"] == "HEALTHY"
