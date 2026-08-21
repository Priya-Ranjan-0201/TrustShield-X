"""
Cyber Crisis Command & AI Security Copilot API Router (Phase 36)
================================================================
Exposes REST endpoints for crisis lifecycle operations, command roles, chronological timelines,
situational awareness, response option analysis, communication drafting & approval,
recovery verification, threat hunt generation, and evidence-grounded Copilot querying.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from pydantic import BaseModel

from app.services.cyber_crisis_command import (
    cyber_crisis_command_engine,
    crisis_escalation_engine,
    crisis_communication_engine,
    crisis_decision_engine,
    crisis_recovery_engine,
    truthshield_security_copilot,
)

router = APIRouter(prefix="/cyber-crisis-command", tags=["Cyber Crisis Command & AI Security Copilot"])


# 1. Crisis Declaration & Lifecycle
@router.post("/declare", response_model=Dict[str, Any])
async def declare_crisis(data: Dict[str, Any]):
    return cyber_crisis_command_engine.declare_crisis(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        incident_ids=data.get("incident_ids", ["INC-101", "INC-102"]),
        declared_by=data.get("declared_by", "SECOPS-COMMANDER"),
        declaration_reason=data.get("declaration_reason", "Multi-vector lateral intrusion attempt"),
        severity=data.get("severity", "SEV_1"),
        affected_scope=data.get("affected_scope")
    )


@router.get("/list/{tenant_id}", response_model=List[Dict[str, Any]])
async def list_crises(tenant_id: str):
    return cyber_crisis_command_engine.list_crises(tenant_id)


@router.get("/{tenant_id}/{crisis_id}", response_model=Dict[str, Any])
async def get_crisis(tenant_id: str, crisis_id: str):
    crisis = cyber_crisis_command_engine.get_crisis(crisis_id, tenant_id)
    if not crisis:
        raise HTTPException(status_code=404, detail="Crisis not found")
    return crisis


@router.post("/transition", response_model=Dict[str, Any])
async def transition_lifecycle_state(data: Dict[str, Any]):
    return cyber_crisis_command_engine.transition_lifecycle_state(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        new_state=data.get("new_state", "CONTAINMENT"),
        actor=data.get("actor", "SECOPS-COMMANDER"),
        reason=data.get("reason", "Containment controls initiated")
    )


# 2. Command Structure & Roles
@router.post("/roles/assign", response_model=Dict[str, Any])
async def assign_role(data: Dict[str, Any]):
    return cyber_crisis_command_engine.assign_role(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        role=data.get("role", "SECURITY_LEAD"),
        assignee=data.get("assignee", "lead-analyst@truthshield.io"),
        assigned_by=data.get("assigned_by", "SECOPS-COMMANDER")
    )


# 3. Timeline & Situational Awareness
@router.post("/timeline/event", response_model=Dict[str, Any])
async def add_timeline_event(data: Dict[str, Any]):
    return cyber_crisis_command_engine.add_timeline_event(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        event_type=data.get("event_type", "INVESTIGATION"),
        description=data.get("description", "Memory dump acquired from API gateway host"),
        source=data.get("source", "FORENSICS_TOOL"),
        actor=data.get("actor", "FORENSICS_LEAD"),
        evidence_reference=data.get("evidence_reference")
    )


@router.get("/timeline/{tenant_id}/{crisis_id}", response_model=List[Dict[str, Any]])
async def get_timeline(tenant_id: str, crisis_id: str):
    return cyber_crisis_command_engine.get_timeline(crisis_id, tenant_id)


@router.get("/situational-awareness/{tenant_id}/{crisis_id}", response_model=Dict[str, Any])
async def get_situational_awareness(tenant_id: str, crisis_id: str):
    return cyber_crisis_command_engine.generate_situational_awareness(crisis_id, tenant_id)


# 4. Decision Intelligence & Response Options
@router.post("/decisions/record", response_model=Dict[str, Any])
async def record_decision(data: Dict[str, Any]):
    return crisis_decision_engine.record_decision(
        decision_id=data.get("decision_id", "DEC-01"),
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        question=data.get("question", "Should we isolate DEV-01 or enforce microsegmentation?"),
        options=data.get("options", []),
        selected_option_id=data.get("selected_option_id", "OPT-A"),
        decision_maker=data.get("decision_maker", "INCIDENT_COMMANDER"),
        rationale=data.get("rationale", "Option A minimizes business downtime while eliminating 4 attack paths")
    )


@router.post("/decisions/options/analyze", response_model=List[Dict[str, Any]])
async def analyze_response_options(data: Dict[str, Any]):
    return crisis_decision_engine.analyze_response_options(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        target_asset=data.get("target_asset", "API-GATEWAY-PROD"),
        threat_scenario=data.get("threat_scenario", "APT29_RANSOMWARE")
    )


# 5. Communications & Fact Governance
@router.post("/communications/draft", response_model=Dict[str, Any])
async def create_communication_draft(data: Dict[str, Any]):
    return crisis_communication_engine.create_communication_draft(
        comm_id=data.get("comm_id", "COMM-01"),
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        comm_type=data.get("comm_type", "EXECUTIVE_BRIEFING"),
        audience=data.get("audience", "Executive Crisis Board"),
        confirmed_facts=data.get("confirmed_facts", ["Containment active", "Zero data loss"]),
        suspected_facts=data.get("suspected_facts", ["APT29 actor attribution"]),
        unknowns=data.get("unknowns", ["Exact Initial Ingress vector"]),
        draft_content=data.get("draft_content", "Executive Briefing summary...")
    )


@router.post("/communications/approve", response_model=Dict[str, Any])
async def approve_communication(data: Dict[str, Any]):
    return crisis_communication_engine.approve_communication(
        comm_id=data.get("comm_id", "COMM-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        approver=data.get("approver", "CISO_LEAD")
    )


@router.post("/communications/send", response_model=Dict[str, Any])
async def send_communication(data: Dict[str, Any]):
    return crisis_communication_engine.send_communication(
        comm_id=data.get("comm_id", "COMM-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        sender=data.get("sender", "COMMUNICATIONS_LEAD")
    )


# 6. Recovery & Verification
@router.post("/recovery/task", response_model=Dict[str, Any])
async def create_recovery_task(data: Dict[str, Any]):
    return crisis_recovery_engine.create_recovery_task(
        task_id=data.get("task_id", "REC-01"),
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        title=data.get("title", "Restore Worker Node 03 from clean image"),
        subsystem=data.get("subsystem", "APPLICATION"),
        owner=data.get("owner", "IT_OPERATIONS")
    )


@router.post("/recovery/verify", response_model=Dict[str, Any])
async def verify_recovery(data: Dict[str, Any]):
    return crisis_recovery_engine.verify_recovery(
        crisis_id=data.get("crisis_id", "CRISIS-01"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        verification_telemetry=data.get("verification_telemetry")
    )


# 7. AI Security Copilot
@router.post("/copilot/query", response_model=Dict[str, Any])
async def query_copilot(data: Dict[str, Any]):
    return truthshield_security_copilot.query_copilot(
        query=data.get("query", "What is the current containment status?"),
        tenant_id=data.get("tenant_id", "tenant-default"),
        user_id=data.get("user_id", "user-analyst"),
        mode=data.get("mode", "SOC_ANALYST"),
        context=data.get("context")
    )


@router.post("/copilot/hunt", response_model=Dict[str, Any])
async def generate_hunt_hypothesis(data: Dict[str, Any]):
    return truthshield_security_copilot.generate_hunt_hypothesis(
        target_pattern=data.get("target_pattern", "Encoded PowerShell Lateral Execution"),
        tenant_id=data.get("tenant_id", "tenant-default")
    )


@router.post("/copilot/detection-rule", response_model=Dict[str, Any])
async def generate_detection_rule(data: Dict[str, Any]):
    return truthshield_security_copilot.generate_detection_rule(
        threat_name=data.get("threat_name", "LockBit Ransomware"),
        tenant_id=data.get("tenant_id", "tenant-default")
    )
