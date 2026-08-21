"""
TruthShield X — Phase 36: Cyber Crisis Command & AI Copilot Pydantic Models
===========================================================================
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import datetime


class CrisisDeclarationRequest(BaseModel):
    crisis_id: str = Field(..., description="Unique crisis identifier")
    tenant_id: str = Field(..., description="Tenant identifier")
    incident_ids: List[str] = Field(default_factory=list, description="Associated incident identifiers")
    declared_by: str = Field(..., description="Actor declaring crisis")
    declaration_reason: str = Field(..., description="Reason for declaring crisis")
    severity: str = Field(default="SEV_1", description="Severity: SEV_1, SEV_2, SEV_3, SEV_4, INFORMATIONAL")
    affected_scope: Dict[str, Any] = Field(default_factory=dict, description="Affected assets, services, and regions")


class CrisisRoleAssignmentRequest(BaseModel):
    crisis_id: str
    tenant_id: str
    role: str  # INCIDENT_COMMANDER, SECURITY_LEAD, SOC_LEAD, FORENSICS_LEAD, IT_OPERATIONS, NETWORK_LEAD, IAM_LEAD, LEGAL, COMPLIANCE, COMMUNICATIONS, EXECUTIVE_SPONSOR, BUSINESS_OWNER
    assignee: str
    assigned_by: str


class TimelineEventRequest(BaseModel):
    crisis_id: str
    tenant_id: str
    event_type: str  # ALERT, OBSERVATION, EVIDENCE, INVESTIGATION, DECISION, ACTION, APPROVAL, RESPONSE, VERIFICATION, RECOVERY
    description: str
    source: str
    actor: str = "System"
    evidence_reference: Optional[str] = None


class DecisionRequest(BaseModel):
    decision_id: str
    crisis_id: str
    tenant_id: str
    question: str
    options: List[Dict[str, Any]]
    recommendation: Optional[str] = None
    decision_maker: str
    approval: Optional[str] = None


class CommunicationDraftRequest(BaseModel):
    comm_id: str
    crisis_id: str
    tenant_id: str
    comm_type: str  # INTERNAL_SECURITY, EXECUTIVE_BRIEFING, OPERATIONAL, CUSTOMER_DRAFT, REGULATORY_DRAFT
    audience: str
    confirmed_facts: List[str] = Field(default_factory=list)
    suspected_facts: List[str] = Field(default_factory=list)
    unknowns: List[str] = Field(default_factory=list)
    draft_content: str


class RecoveryTaskRequest(BaseModel):
    task_id: str
    crisis_id: str
    tenant_id: str
    title: str
    subsystem: str
    owner: str
    dependencies: List[str] = Field(default_factory=list)


class CopilotQueryRequest(BaseModel):
    query_id: Optional[str] = None
    tenant_id: str = "tenant-default"
    user_id: str = "user-analyst"
    mode: str = "SOC_ANALYST"  # SOC_ANALYST, INCIDENT_RESPONDER, THREAT_HUNTER, FORENSICS_ANALYST, SECURITY_ENGINEER, RISK_ANALYST, COMPLIANCE_ANALYST, EXECUTIVE, CRISIS_COMMANDER
    query: str
    crisis_id: Optional[str] = None
    incident_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None
