"""
TruthShield X — Phase 15 Mission Control & Cyber Crisis Command Models

Extends existing SOC operations models (Phase 4) with Incident Command,
Crisis Declaration, Evidence Classification, Response Planning, Recovery,
and Lessons Learned DTOs.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Phase 15 Type Literals
# ============================================================================

CommandStatusLiteral = Literal[
    "DETECTED",
    "TRIAGE",
    "INVESTIGATING",
    "CONFIRMED",
    "CONTAINMENT",
    "ERADICATION",
    "RECOVERY",
    "VALIDATION",
    "MONITORING",
    "RESOLVED",
    "CLOSED",
]

VALID_COMMAND_TRANSITIONS: Dict[str, List[str]] = {
    "DETECTED": ["TRIAGE"],
    "TRIAGE": ["INVESTIGATING", "CLOSED"],
    "INVESTIGATING": ["CONFIRMED", "CLOSED"],
    "CONFIRMED": ["CONTAINMENT"],
    "CONTAINMENT": ["ERADICATION"],
    "ERADICATION": ["RECOVERY"],
    "RECOVERY": ["VALIDATION"],
    "VALIDATION": ["MONITORING", "RECOVERY"],
    "MONITORING": ["RESOLVED"],
    "RESOLVED": ["CLOSED"],
    "CLOSED": [],
}

CommandSeverityLiteral = Literal[
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
    "CRISIS",
]

DeclarationLevelLiteral = Literal[
    "OBSERVATION",
    "ALERT",
    "CASE",
    "INCIDENT",
    "MAJOR_INCIDENT",
    "CRISIS",
]

EvidenceClassificationLiteral = Literal[
    "VERIFIED",
    "STRONGLY_SUPPORTED",
    "INFERRED",
    "PREDICTED",
    "SIMULATED",
    "UNVERIFIED",
    "CONFLICTING",
]

ResponsePlanStatusLiteral = Literal[
    "PROPOSED",
    "SIMULATING",
    "AWAITING_APPROVAL",
    "APPROVED",
    "REJECTED",
    "EXECUTING",
    "SUCCEEDED",
    "FAILED",
    "PARTIALLY_SUCCEEDED",
    "ROLLED_BACK",
    "VERIFICATION_FAILED",
]

SafetyScoreLiteral = Literal[
    "SAFE",
    "REVIEW_REQUIRED",
    "HIGH_RISK",
    "BLOCKED",
]

AutomationLevelLiteral = Literal[
    "LEVEL_0_MANUAL",
    "LEVEL_1_ASSISTED",
    "LEVEL_2_APPROVAL_REQUIRED",
    "LEVEL_3_CONTROLLED_AUTOMATION",
    "LEVEL_4_FULLY_AUTOMATED_SAFE",
]

RootCauseCategoryLiteral = Literal[
    "CONTROL_FAILURE",
    "CONFIGURATION",
    "HUMAN_ERROR",
    "SOFTWARE_DEFECT",
    "THIRD_PARTY",
    "PROCESS_FAILURE",
    "UNKNOWN",
]

CrisisPlaybookTypeLiteral = Literal[
    "PHISHING_CAMPAIGN",
    "ACCOUNT_TAKEOVER",
    "MALWARE_INCIDENT",
    "PAYMENT_FRAUD",
    "DATA_EXPOSURE",
    "API_COMPROMISE",
    "IDENTITY_ABUSE",
    "SUPPLY_CHAIN_INCIDENT",
    "THIRD_PARTY_OUTAGE",
    "CLOUD_FAILURE",
    "MASS_SERVICE_OUTAGE",
    "MULTI_TENANT_SECURITY_EVENT",
]


# ============================================================================
# Incident Command
# ============================================================================

class IncidentCommandDTO(BaseModel):
    """Incident Command structure (Section 3)."""
    model_config = ConfigDict(from_attributes=True)

    incident_command_id: str = Field(default_factory=lambda: f"cmd_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    incident_id: str = ""
    severity: CommandSeverityLiteral = "MEDIUM"
    confidence: float = 0.5
    evidence_strength: float = 0.5
    command_status: CommandStatusLiteral = "DETECTED"
    declaration_level: DeclarationLevelLiteral = "OBSERVATION"
    incident_commander: str = ""
    technical_lead: str = ""
    communications_lead: str = ""
    recovery_lead: str = ""
    governance_lead: str = ""
    parent_incident_id: Optional[str] = None
    child_incident_ids: List[str] = Field(default_factory=list)
    related_incident_ids: List[str] = Field(default_factory=list)
    triggering_signals: List[str] = Field(default_factory=list)
    affected_asset_ids: List[str] = Field(default_factory=list)
    affected_service_ids: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    declared_at: Optional[str] = None
    resolved_at: Optional[str] = None


# ============================================================================
# Incident Evidence Room & Evidence Conflicts
# ============================================================================

class IncidentEvidenceItemDTO(BaseModel):
    """Classified evidence item within an incident evidence room (Section 10-11)."""
    model_config = ConfigDict(from_attributes=True)

    evidence_item_id: str = Field(default_factory=lambda: f"evi_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    source: str = ""
    source_type: str = "SYSTEM"
    classification: EvidenceClassificationLiteral = "UNVERIFIED"
    confidence: float = 0.5
    description: str = ""
    payload: Dict[str, Any] = Field(default_factory=dict)
    related_entity_ids: List[str] = Field(default_factory=list)
    related_alert_ids: List[str] = Field(default_factory=list)
    related_hunt_ids: List[str] = Field(default_factory=list)
    provenance: str = ""
    collected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_immutable: bool = True


class EvidenceConflictDTO(BaseModel):
    """Conflicting evidence record (Section 12)."""
    model_config = ConfigDict(from_attributes=True)

    conflict_id: str = Field(default_factory=lambda: f"cnf_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    evidence_a_id: str = ""
    evidence_b_id: str = ""
    source_a_reliability: float = 0.5
    source_b_reliability: float = 0.5
    conflict_description: str = ""
    resolution_status: Literal["OPEN", "UNDER_INVESTIGATION", "RESOLVED", "ACCEPTED_DIVERGENCE"] = "OPEN"
    investigator_note: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentEvidenceRoomDTO(BaseModel):
    """Aggregated evidence room for an incident (Section 10)."""
    model_config = ConfigDict(from_attributes=True)

    incident_command_id: str = ""
    evidence_items: List[IncidentEvidenceItemDTO] = Field(default_factory=list)
    conflicts: List[EvidenceConflictDTO] = Field(default_factory=list)
    total_verified: int = 0
    total_unverified: int = 0
    total_conflicting: int = 0


# ============================================================================
# Business Service Impact
# ============================================================================

class BusinessServiceImpactDTO(BaseModel):
    """Business service impact assessment (Section 15)."""
    model_config = ConfigDict(from_attributes=True)

    service_id: str = ""
    service_name: str = ""
    owner: str = ""
    criticality: Literal["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"] = "UNKNOWN"
    availability_impact: Literal["TOTAL_OUTAGE", "DEGRADED", "MINIMAL", "NONE", "UNKNOWN"] = "UNKNOWN"
    dependency_impact: Literal["CASCADE_RISK", "ISOLATED", "UNKNOWN"] = "UNKNOWN"
    affected_asset_ids: List[str] = Field(default_factory=list)
    business_impact_known: bool = False


# ============================================================================
# Crisis Declaration
# ============================================================================

class CrisisDeclarationDTO(BaseModel):
    """Crisis declaration record (Section 16)."""
    model_config = ConfigDict(from_attributes=True)

    crisis_id: str = Field(default_factory=lambda: f"crs_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    incident_command_ids: List[str] = Field(default_factory=list)
    crisis_status: Literal["NOT_DECLARED", "DECLARED", "ESCALATED", "RECOVERING", "RESOLVED"] = "NOT_DECLARED"
    trigger_reason: str = ""
    policy_thresholds_met: List[str] = Field(default_factory=list)
    affected_services_count: int = 0
    declared_by: str = ""
    declared_at: Optional[str] = None
    resolved_at: Optional[str] = None


# ============================================================================
# Response Plan & Safety Score
# ============================================================================

class ResponseOptionDTO(BaseModel):
    """Single response option within a plan (Section 19-20)."""
    model_config = ConfigDict(from_attributes=True)

    option_id: str = Field(default_factory=lambda: f"opt_{uuid.uuid4().hex[:8]}")
    objective: str = ""
    scope: str = ""
    expected_benefit: str = ""
    potential_collateral_impact: str = ""
    dependencies: List[str] = Field(default_factory=list)
    reversibility: Literal["FULLY_REVERSIBLE", "PARTIALLY_REVERSIBLE", "IRREVERSIBLE", "UNKNOWN"] = "UNKNOWN"
    confidence: float = 0.5
    required_approvals: List[str] = Field(default_factory=list)
    verification_method: str = ""
    risk_reduction_score: float = 0.0
    blast_radius_reduction: float = 0.0
    service_disruption_score: float = 0.0
    execution_complexity: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    automation_level: AutomationLevelLiteral = "LEVEL_2_APPROVAL_REQUIRED"
    safety_score: SafetyScoreLiteral = "REVIEW_REQUIRED"
    simulation_result: Optional[Dict[str, Any]] = None
    status: ResponsePlanStatusLiteral = "PROPOSED"


class ResponsePlanDTO(BaseModel):
    """Multi-option response plan for an incident (Section 19)."""
    model_config = ConfigDict(from_attributes=True)

    plan_id: str = Field(default_factory=lambda: f"pln_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    options: List[ResponseOptionDTO] = Field(default_factory=list)
    recommended_option_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Crisis Communications & Escalation
# ============================================================================

class CrisisCommunicationDTO(BaseModel):
    """Crisis communication record (Section 31-32)."""
    model_config = ConfigDict(from_attributes=True)

    communication_id: str = Field(default_factory=lambda: f"comm_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    channel: Literal["INTERNAL", "SECURITY_TEAM", "EXECUTIVE", "SERVICE_OWNER", "GOVERNANCE"] = "INTERNAL"
    confirmation_level: Literal["CONFIRMED", "SUSPECTED", "UNKNOWN"] = "UNKNOWN"
    subject: str = ""
    body: str = ""
    evidence_references: List[str] = Field(default_factory=list)
    sent_by: str = ""
    sent_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IncidentEscalationDTO(BaseModel):
    """Incident escalation record (Section 34)."""
    model_config = ConfigDict(from_attributes=True)

    escalation_id: str = Field(default_factory=lambda: f"esc_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    trigger: Literal["SEVERITY", "CONFIDENCE", "TIME", "BUSINESS_IMPACT", "CONTROL_FAILURE", "SLA", "UNRESOLVED_RESPONSE"] = "SEVERITY"
    from_level: str = ""
    to_level: str = ""
    escalated_by: str = "SYSTEM"
    escalated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Decision Log & AI Recommendation Audit
# ============================================================================

class IncidentDecisionLogDTO(BaseModel):
    """Auditable decision record (Section 38-39)."""
    model_config = ConfigDict(from_attributes=True)

    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    decision: str = ""
    alternatives: List[str] = Field(default_factory=list)
    reasoning: str = ""
    evidence_references: List[str] = Field(default_factory=list)
    decision_maker: str = ""
    is_ai_recommendation: bool = False
    ai_model_version: Optional[str] = None
    ai_confidence: Optional[float] = None
    ai_limitations: List[str] = Field(default_factory=list)
    human_decision: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Incident Recovery & Residual Risk
# ============================================================================

class IncidentRecoveryDTO(BaseModel):
    """Recovery tracking record (Section 48-50)."""
    model_config = ConfigDict(from_attributes=True)

    recovery_id: str = Field(default_factory=lambda: f"rec_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    recovery_sequence: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)
    restored_services: List[str] = Field(default_factory=list)
    restored_assets: List[str] = Field(default_factory=list)
    service_health_verified: bool = False
    security_controls_verified: bool = False
    monitoring_restored: bool = False
    audit_restored: bool = False
    tenant_isolation_verified: bool = False
    pre_incident_risk: float = 0.0
    incident_risk: float = 0.0
    post_response_risk: float = 0.0
    residual_risk: float = 0.0
    residual_risk_basis: Literal["MEASURED", "ESTIMATED", "SIMULATED"] = "ESTIMATED"
    recovery_complete: bool = False
    verified_at: Optional[str] = None


# ============================================================================
# Lessons Learned & Root Cause Analysis
# ============================================================================

class RootCauseAnalysisDTO(BaseModel):
    """Root cause analysis record (Section 52-53)."""
    model_config = ConfigDict(from_attributes=True)

    rca_id: str = Field(default_factory=lambda: f"rca_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    primary_cause: RootCauseCategoryLiteral = "UNKNOWN"
    contributing_factors: List[str] = Field(default_factory=list)
    enabling_conditions: List[str] = Field(default_factory=list)
    failed_controls: List[str] = Field(default_factory=list)
    missing_controls: List[str] = Field(default_factory=list)
    evidence_references: List[str] = Field(default_factory=list)
    confidence: float = 0.5
    analyst: str = ""
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class LessonsLearnedDTO(BaseModel):
    """Post-incident lessons learned record (Section 51)."""
    model_config = ConfigDict(from_attributes=True)

    lessons_id: str = Field(default_factory=lambda: f"lsn_{uuid.uuid4().hex[:8]}")
    incident_command_id: str = ""
    what_happened: str = ""
    what_worked: List[str] = Field(default_factory=list)
    what_failed: List[str] = Field(default_factory=list)
    control_failures: List[str] = Field(default_factory=list)
    response_delays: List[str] = Field(default_factory=list)
    detection_gaps: List[str] = Field(default_factory=list)
    governance_gaps: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    root_cause_analysis: Optional[RootCauseAnalysisDTO] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Crisis Readiness Score
# ============================================================================

class CrisisReadinessScoreDTO(BaseModel):
    """Multi-dimensional crisis readiness scorecard (Section 58)."""
    model_config = ConfigDict(from_attributes=True)

    detection_readiness: float = 0.0
    response_readiness: float = 0.0
    communication_readiness: float = 0.0
    recovery_readiness: float = 0.0
    governance_readiness: float = 0.0
    control_health_readiness: float = 0.0
    dr_readiness: float = 0.0
    human_readiness: float = 0.0
    overall_readiness: float = 0.0
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Mission Control Summary
# ============================================================================

class MissionControlSummaryDTO(BaseModel):
    """Aggregated mission control dashboard state (Section 59)."""
    model_config = ConfigDict(from_attributes=True)

    active_incidents: int = 0
    critical_alerts: int = 0
    crisis_status: str = "NO_ACTIVE_CRISIS"
    services_at_risk: int = 0
    pending_response_actions: int = 0
    approvals_required: int = 0
    active_recoveries: int = 0
    residual_risk_score: float = 0.0
    crisis_readiness: Optional[CrisisReadinessScoreDTO] = None
    assessed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
