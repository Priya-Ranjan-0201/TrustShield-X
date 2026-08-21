"""
TruthShield X — Phase 13 Continuous Security Control Assurance & Drift Detection Data Models
"""

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone


ControlCategoryLiteral = Literal[
    "PREVENTIVE",
    "DETECTIVE",
    "CORRECTIVE",
    "RECOVERY",
    "GOVERNANCE",
    "ACCESS_CONTROL",
    "DATA_PROTECTION",
    "MONITORING",
    "AI_SECURITY",
    "TENANT_ISOLATION",
    "AUDIT",
    "INCIDENT_RESPONSE",
    "DISASTER_RECOVERY",
]

ControlLifecycleLiteral = Literal[
    "REGISTERED",
    "CONFIGURED",
    "ACTIVE",
    "TESTING",
    "VERIFIED",
    "DEGRADED",
    "FAILED",
    "UNKNOWN",
    "RETIRED",
]

VerificationStateLiteral = Literal[
    "DOCUMENTED",
    "CONFIGURED",
    "OBSERVED",
    "TESTED",
    "VERIFIED",
    "DEGRADED",
    "FAILED",
    "UNKNOWN",
    "NOT_APPLICABLE",
]

TestResultStatusLiteral = Literal[
    "PASS",
    "FAIL",
    "BLOCKED",
    "SKIPPED",
    "NOT_APPLICABLE",
    "UNKNOWN",
]

DriftSeverityLiteral = Literal[
    "INFORMATIONAL",
    "LOW",
    "MEDIUM",
    "HIGH",
    "CRITICAL",
]

FreshnessStateLiteral = Literal[
    "CURRENT",
    "DUE_SOON",
    "OVERDUE",
    "NEVER_TESTED",
]


class SecurityControlRegistryDTO(BaseModel):
    control_id: str
    tenant_id: str = "PLATFORM_SCOPE"
    name: str
    category: ControlCategoryLiteral
    description: str
    owner: str = "security_operations"
    status: ControlLifecycleLiteral = "ACTIVE"
    criticality: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "HIGH"
    verification_state: VerificationStateLiteral = "VERIFIED"
    last_verified: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    next_verification: Optional[str] = None
    evidence_count: int = 1
    version: int = 1
    freshness: FreshnessStateLiteral = "CURRENT"


class ControlAssertionDTO(BaseModel):
    assertion_id: str
    control_id: str
    expression: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = "CRITICAL"
    verification_method: str
    expected_result: str
    frequency: str = "HOURLY"
    last_evaluated_state: Literal["SATISFIED", "VIOLATED", "UNKNOWN"] = "SATISFIED"


class SecurityInvariantDTO(BaseModel):
    invariant_id: str
    title: str
    description: str
    is_satisfied: bool = True
    criticality: Literal["HIGH", "CRITICAL"] = "CRITICAL"
    last_evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evidence: Dict[str, Any] = Field(default_factory=dict)


class ControlTestExecutionDTO(BaseModel):
    execution_id: str
    test_id: str
    control_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    environment: str = "STAGING"
    expected: str
    actual: str
    result: TestResultStatusLiteral
    evidence: Dict[str, Any] = Field(default_factory=dict)
    duration_ms: int = 12
    operator: str = "AUTONOMOUS_ASSURANCE_SCHEDULER"


class SecurityBaselineDTO(BaseModel):
    baseline_id: str
    version: int = 1
    owner: str = "chief_information_security_officer"
    approved_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    approved_by: str = "security_lead"
    configuration_hash: str
    parameters: Dict[str, Any] = Field(default_factory=dict)


class SecurityDriftDTO(BaseModel):
    drift_id: str
    control_id: str
    drift_type: Literal["EXPECTED_CHANGE", "CONFIGURATION_DRIFT", "BEHAVIOR_DRIFT", "PERFORMANCE_DRIFT", "UNKNOWN_DRIFT"]
    severity: DriftSeverityLiteral
    baseline_value: str
    current_value: str
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    status: Literal["DETECTED", "APPROVED", "REMEDIATING", "REMEDIATED", "ACKNOWLEDGED"] = "DETECTED"
    owner: str = "secops_lead"


class SecuritySLODTO(BaseModel):
    slo_id: str
    target_metric: str  # DETECTION_AVAILABILITY, MONITORING_UPTIME, ALERT_DELIVERY, BACKUP_FRESHNESS
    target_percentage: float = 99.9
    actual_percentage: float = 99.95
    error_budget_remaining: float = 85.0
    status: Literal["MET", "AT_RISK", "BREACHED"] = "MET"
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityAssuranceSummaryDTO(BaseModel):
    overall_assurance_score: float  # 0.0 - 100.0
    control_coverage_percentage: float
    total_controls: int
    controls_verified: int
    controls_degraded: int
    controls_failed: int
    controls_unknown: int
    active_drifts_count: int
    invariants_satisfied_count: int
    invariants_violated_count: int
    last_certified_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
