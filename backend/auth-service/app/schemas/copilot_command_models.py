"""
TruthShield X — Security Copilot & Cyber Command Center Models (Phase 20).

Strictly typed Pydantic models for Role-Aware Context, Answer Contracts with Evidence Citations,
Request Classification, Investigation Workflows, Threat Hunting Queries, Action Plans & Approvals,
Verification, Executive Briefings, CISO & SOC Command Centers, Tool Registries, and Quality Evaluation.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 20)
# ============================================================================

RequestClassificationLiteral = Literal[
    "INFORMATION",
    "INVESTIGATION",
    "ANALYSIS",
    "HUNT",
    "RECOMMENDATION",
    "SIMULATION",
    "ACTION_REQUEST",
    "REPORTING",
    "GOVERNANCE",
    "INCIDENT_RESPONSE",
    "EXECUTIVE_QUERY",
    "ASK_CLARIFICATION",
]

CopilotRoleLiteral = Literal[
    "ANALYST",
    "HUNTER",
    "INCIDENT_RESPONDER",
    "ENGINEER",
    "GOVERNANCE",
    "ADMIN",
    "CISO",
    "EXECUTIVE",
]

EpistemicStatusLiteral = Literal[
    "OBSERVED",
    "VERIFIED",
    "CORRELATED",
    "INFERRED",
    "HYPOTHESIS",
    "PREDICTED",
    "SIMULATED",
    "RECOMMENDED",
    "EXECUTED",
    "VERIFIED_AFTER_ACTION",
    "UNKNOWN",
]

ActionStateLiteral = Literal[
    "PROPOSED",
    "APPROVAL_REQUIRED",
    "APPROVED",
    "EXECUTED",
    "VERIFIED",
    "FAILED",
    "ROLLED_BACK",
    "BLOCKED",
]


# ============================================================================
# Citations, Context & Message DTOs
# ============================================================================

class EvidenceCitationDTO(BaseModel):
    evidence_id: str
    source_id: str
    object_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    snippet: str
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)

    model_config = ConfigDict(frozen=True)


class AnswerContractDTO(BaseModel):
    answer: str
    evidence: List[EvidenceCitationDTO] = Field(default_factory=list)
    confidence: float = Field(default=0.88, ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    unknown_areas: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    epistemic_status: EpistemicStatusLiteral = "INFERRED"

    model_config = ConfigDict(frozen=True)


class CopilotMessageDTO(BaseModel):
    message_id: str = Field(default_factory=lambda: f"msg_{uuid.uuid4().hex[:10]}")
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    citations: List[EvidenceCitationDTO] = Field(default_factory=list)
    epistemic_status: Optional[EpistemicStatusLiteral] = None

    model_config = ConfigDict(frozen=True)


class CopilotContextDTO(BaseModel):
    tenant_id: str = "default_tenant"
    user_id: str = "usr_analyst_01"
    user_role: CopilotRoleLiteral = "ANALYST"
    permissions: List[str] = Field(default_factory=lambda: ["copilot.read", "copilot.query", "copilot.investigate"])
    current_incident: Optional[str] = None
    selected_asset: Optional[str] = None
    selected_campaign: Optional[str] = None
    selected_investigation: Optional[str] = None
    environment: str = "PRODUCTION"
    relevant_policies: List[str] = Field(default_factory=list)
    relevant_evidence: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class CopilotSessionDTO(BaseModel):
    session_id: str = Field(default_factory=lambda: f"session_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    user_id: str = "usr_analyst_01"
    user_role: CopilotRoleLiteral = "ANALYST"
    active_incident_id: Optional[str] = None
    active_asset_id: Optional[str] = None
    active_investigation_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    messages: List[CopilotMessageDTO] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Investigation, Hunting & Action Planning DTOs
# ============================================================================

class InvestigationSummaryDTO(BaseModel):
    investigation_id: str = Field(default_factory=lambda: f"inv_{uuid.uuid4().hex[:10]}")
    current_assessment: str
    what_we_know: List[str] = Field(default_factory=list)
    what_we_do_not_know: List[str] = Field(default_factory=list)
    supporting_evidence: List[str] = Field(default_factory=list)
    contradictions: List[str] = Field(default_factory=list)
    likely_hypotheses: List[str] = Field(default_factory=list)
    next_best_questions: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class NextBestInvestigationDTO(BaseModel):
    investigation_id: str
    action_title: str
    target_entity: str
    expected_information_gain: float = Field(default=0.85, ge=0.0, le=1.0)
    security_risk_reduction: float = Field(default=0.80, ge=0.0, le=1.0)
    urgency: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    feasibility: Literal["EASY", "MODERATE", "HARD"] = "EASY"
    priority_score: float = 0.88

    model_config = ConfigDict(frozen=True)


class GeneratedQueryDTO(BaseModel):
    query_id: str = Field(default_factory=lambda: f"qry_{uuid.uuid4().hex[:8]}")
    query_type: Literal["SQL", "LOG", "GRAPH", "SIEM"]
    query_text: str
    is_read_only: bool = True
    target_scope: str
    syntax_valid: bool = True
    safety_status: Literal["SAFE", "BLOCKED_MUTATION", "SCOPE_VIOLATION"] = "SAFE"

    model_config = ConfigDict(frozen=True)


class CopilotActionPlanDTO(BaseModel):
    plan_id: str = Field(default_factory=lambda: f"act_plan_{uuid.uuid4().hex[:10]}")
    session_id: str
    action_type: str
    target_resource: str
    reason: str
    evidence_ids: List[str] = Field(default_factory=list)
    expected_benefit: str
    possible_impact: str
    simulation_id: Optional[str] = None
    rollback_steps: List[str] = Field(default_factory=list)
    approval_status: ActionStateLiteral = "APPROVAL_REQUIRED"
    required_approval_tier: str = "TIER_2_FOUR_EYES"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class CopilotActionVerificationDTO(BaseModel):
    plan_id: str
    action_state: ActionStateLiteral = "VERIFIED"
    verification_result: str
    actual_state: str
    expected_state: str
    has_divergence: bool = False
    rollback_status: str = "READY"
    verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Tool Registry, Executive Intelligence & Quality DTOs
# ============================================================================

class CopilotToolDefinitionDTO(BaseModel):
    tool_id: str
    name: str
    description: str
    required_permission: str
    scope: str
    risk_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "LOW"
    is_read_only: bool = True
    requires_approval: bool = False

    model_config = ConfigDict(frozen=True)


class CopilotToolCallDTO(BaseModel):
    call_id: str = Field(default_factory=lambda: f"call_{uuid.uuid4().hex[:10]}")
    tool_id: str
    arguments: Dict[str, Any] = Field(default_factory=dict)
    tenant_id: str
    user_id: str
    result: Dict[str, Any] = Field(default_factory=dict)
    is_authorized: bool = True
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ExecutiveBriefingDTO(BaseModel):
    brief_id: str = Field(default_factory=lambda: f"brief_{uuid.uuid4().hex[:10]}")
    brief_type: Literal["DAILY_BRIEF", "CHANGE_BRIEF", "RISK_BRIEF"]
    tenant_id: str
    business_impact: str
    security_impact: str
    operational_impact: str
    financial_impact: str = "FINANCIAL IMPACT UNKNOWN"
    top_risks: List[str] = Field(default_factory=list)
    decisions_required: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class CISOCommandCenterSummaryDTO(BaseModel):
    tenant_id: str
    security_posture_score: float = 87.5
    active_incidents_count: int = 2
    top_threats: List[str] = Field(default_factory=list)
    exposure_index: float = 14.2
    control_health_pct: float = 94.0
    resilience_score: float = 88.5
    knowledge_health_score: float = 93.8
    open_decisions_count: int = 1
    trend: Literal["IMPROVING", "STABLE", "DEGRADING"] = "IMPROVING"
    last_updated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class CopilotQualityEvaluationDTO(BaseModel):
    factual_grounding_score: float = 96.0
    citation_coverage_pct: float = 98.5
    hallucination_rate_pct: float = 0.0
    tool_accuracy_pct: float = 99.0
    refusal_correctness_pct: float = 100.0
    authorization_correctness_pct: float = 100.0
    prompt_injection_resistance_pct: float = 100.0
    average_latency_ms: float = 180.0

    model_config = ConfigDict(frozen=True)
