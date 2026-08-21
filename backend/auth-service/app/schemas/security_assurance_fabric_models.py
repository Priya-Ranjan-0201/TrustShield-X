"""
TruthShield X — Continuous Security Assurance & Control Validation Models (Phase 24).

Strictly typed Pydantic models for Security Controls, Security Assertions, Control Validations,
Security Drift Records, Regression Runs, Baselines, AI Security Assurance, Remediation Plans,
Security Game Days, Security Debt, and Multidimensional Assurance Scorecards.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Phase 24)
# ============================================================================

ControlCategoryLiteral = Literal[
    "IDENTITY",
    "ACCESS_CONTROL",
    "TENANT_ISOLATION",
    "DATA_PROTECTION",
    "ENCRYPTION",
    "AUDIT",
    "DETECTION",
    "MONITORING",
    "INCIDENT_RESPONSE",
    "SOAR",
    "THREAT_INTELLIGENCE",
    "RESILIENCE",
    "BACKUP",
    "RECOVERY",
    "API_SECURITY",
    "APPLICATION_SECURITY",
    "INFRASTRUCTURE",
    "AI_SECURITY",
    "MODEL_SECURITY",
    "GOVERNANCE",
]

ControlCriticalityLiteral = Literal[
    "CRITICAL",
    "HIGH",
    "MEDIUM",
    "LOW",
]

ValidationStatusLiteral = Literal[
    "PASS",
    "FAIL",
    "PARTIAL",
    "NOT_VERIFIED",
    "BLOCKED",
    "ERROR",
    "REMEDIATION_NOT_VERIFIED",
]

DriftTypeLiteral = Literal[
    "CONFIGURATION",
    "AUTHORIZATION",
    "DETECTION",
    "PLAYBOOK",
    "RECOVERY",
    "MODEL",
    "DATA",
]

AssuranceMaturityLiteral = Literal[
    "LEVEL_0_UNKNOWN",
    "LEVEL_1_DOCUMENTED",
    "LEVEL_2_IMPLEMENTED",
    "LEVEL_3_TESTED",
    "LEVEL_4_MEASURED",
    "LEVEL_5_CONTINUOUSLY_VALIDATED",
]


# ============================================================================
# Security Control & Assertion Models
# ============================================================================

class SecurityControlDTO(BaseModel):
    control_id: str = Field(default_factory=lambda: f"ctl_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    name: str
    category: ControlCategoryLiteral = "ACCESS_CONTROL"
    owner: str = "usr_sec_lead"
    criticality: ControlCriticalityLiteral = "CRITICAL"
    implementation_status: Literal["IMPLEMENTED", "PLANNED", "DEPRECATED"] = "IMPLEMENTED"
    validation_status: ValidationStatusLiteral = "PASS"
    expected_behavior: str = "Must reject unauthorized requests with HTTP 403 Forbidden."
    failure_behavior: str = "Unauthorized request permitted (security breach)."
    last_validated: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    next_validation: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence_hashes: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class SecurityAssertionDTO(BaseModel):
    assertion_id: str = Field(default_factory=lambda: f"asrt_{uuid.uuid4().hex[:8]}")
    control_id: str
    statement: str = "Cross-tenant data access is strictly blocked at the datastore layer."
    test_method: str = "SYNTHETIC_CROSS_TENANT_INJECTION"
    acceptable_state: str = "ACCESS_DENIED_EXPLICIT"
    is_validated: bool = True
    last_verified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class ControlValidationResultDTO(BaseModel):
    validation_id: str = Field(default_factory=lambda: f"cval_{uuid.uuid4().hex[:8]}")
    control_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    environment: Literal["UNIT", "INTEGRATION", "STAGING", "ISOLATED_SANDBOX", "PRODUCTION_READ_ONLY"] = "ISOLATED_SANDBOX"
    test_name: str
    expected_result: str
    actual_result: str
    status: ValidationStatusLiteral = "PASS"
    evidence_hash: str = Field(default_factory=lambda: f"sha256_{uuid.uuid4().hex}")
    evidence_details: str = "Validation test executed against sandbox runtime endpoint."

    model_config = ConfigDict(frozen=True)


# ============================================================================
# Security Drift, Baselines & Regression Models
# ============================================================================

class SecurityDriftDTO(BaseModel):
    drift_id: str = Field(default_factory=lambda: f"sdrift_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    drift_type: DriftTypeLiteral = "CONFIGURATION"
    component: str
    description: str
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    is_reconciled: bool = False
    reconciliation_notes: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class SecurityBaselineDTO(BaseModel):
    baseline_id: str = Field(default_factory=lambda: f"sbase_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    version: str = "v1.0.0-PROD-LOCKED"
    immutable_hash: str = Field(default_factory=lambda: f"sha256_{uuid.uuid4().hex}")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    control_states: Dict[str, str] = Field(default_factory=dict)
    is_active: bool = True

    model_config = ConfigDict(frozen=True)


class SecurityRegressionRunDTO(BaseModel):
    regression_id: str = Field(default_factory=lambda: f"sreg_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    trigger_event: str = "PR_MERGE_AUTH_SERVICE"
    changed_components: List[str] = Field(default_factory=list)
    affected_controls: List[str] = Field(default_factory=list)
    tests_executed: int = 40
    passed_count: int = 40
    failed_count: int = 0
    regressions_detected: List[str] = Field(default_factory=list)
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


# ============================================================================
# AI Assurance, Remediation, Game Days, Debt & Scorecard
# ============================================================================

class AIControlAssuranceDTO(BaseModel):
    assurance_id: str = Field(default_factory=lambda: f"aiass_{uuid.uuid4().hex[:8]}")
    model_name: str = "TruthShield_Copilot_LLM_v3"
    prompt_injection_tested: bool = True
    tool_authorization_verified: bool = True
    hallucination_score: float = 0.02
    provenance_coverage: float = 0.99
    status: ValidationStatusLiteral = "PASS"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class RemediationPlanDTO(BaseModel):
    remediation_id: str = Field(default_factory=lambda: f"rem_{uuid.uuid4().hex[:8]}")
    control_id: str
    failure_reason: str
    root_cause_category: Literal["ROOT_CAUSE", "CONTRIBUTING_FACTOR", "CORRELATION", "HYPOTHESIS", "UNKNOWN"] = "ROOT_CAUSE"
    actions: List[str] = Field(default_factory=list)
    is_approved: bool = False
    approver_id: Optional[str] = None
    execution_status: Literal["PENDING", "EXECUTED", "REMEDIATED", "REMEDIATION_NOT_VERIFIED", "FAILED"] = "PENDING"
    revalidated_at: Optional[str] = None

    model_config = ConfigDict(frozen=True)


class SecurityGameDayDTO(BaseModel):
    game_day_id: str = Field(default_factory=lambda: f"gday_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    scenario_name: str = "ADVERSARIAL_CREDENTIAL_STUFFING_AND_LATERAL_MOVEMENT"
    phases_completed: List[str] = Field(default_factory=list)
    mttd_seconds: float = 45.0
    mtta_seconds: float = 120.0
    containment_success: bool = True
    evidence_quality_score: float = 98.5
    status: Literal["PLANNED", "RUNNING", "COMPLETED", "FAILED"] = "COMPLETED"
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)


class SecurityDebtDTO(BaseModel):
    debt_id: str = Field(default_factory=lambda: f"sdebt_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default_tenant"
    unverified_controls_count: int = 0
    outdated_tests_count: int = 0
    stale_playbooks_count: int = 0
    coverage_gaps_count: int = 1
    total_debt_score: float = 12.5
    priority_recommendations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)


class AssuranceScorecardDTO(BaseModel):
    tenant_id: str = "default_tenant"
    overall_score: float = 96.4
    implementation_score: float = 98.0
    validation_score: float = 95.5
    effectiveness_score: float = 96.0
    freshness_score: float = 96.0
    residual_risk_score: float = 3.6
    maturity_level: AssuranceMaturityLiteral = "LEVEL_5_CONTINUOUSLY_VALIDATED"
    scorecard_grade: Literal["EXCELLENT", "ADEQUATE", "NEEDS_IMPROVEMENT", "CRITICAL_RISK"] = "EXCELLENT"
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True)
