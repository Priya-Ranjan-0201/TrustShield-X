"""Pydantic v2 DTO Schemas for Predictive Threat Intelligence, Threat Hunting & Early Warning (Phase 6).

Strictly typed DTOs for Threat Signals, Indicator Lifecycles, Source Reliability, Threat Anomalies,
Early Warnings, Propagation Scoring, Campaign Forecasts, Predictive Risk, Threat Hunting,
and Prediction Calibration.
"""

from typing import List, Dict, Any, Optional, Literal
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Type Literals & Enums (Sections 2, 4, 7, 19)
# ============================================================================

IndicatorLifecycleStateLiteral = Literal[
    "FIRST_SEEN",
    "ACTIVE",
    "STALE",
    "EXPIRED",
    "REVOKED",
    "REVALIDATED",
]

PredictionConfidenceLiteral = Literal[
    "VERY_LOW",
    "LOW",
    "MEDIUM",
    "HIGH",
    "VERY_HIGH",
]

CampaignGrowthStateLiteral = Literal[
    "ACCELERATING",
    "STABLE",
    "DECLINING",
    "DORMANT",
    "REACTIVATED",
]


# ============================================================================
# Section 2 & 4: Threat Signal Normalization & Indicator Lifecycle
# ============================================================================

class ThreatSignalDTO(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{uuid.uuid4().hex[:12]}")
    signal_type: str  # e.g., DOMAIN, APK, URL, IP, PHONE, UPI, CERTIFICATE
    source: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    entity_id: str
    confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    severity: str = "HIGH"  # CRITICAL, HIGH, MEDIUM, LOW, INFORMATIONAL
    provenance: Dict[str, Any] = Field(default_factory=dict)
    tenant_scope: str = "default_tenant"
    lifecycle_state: IndicatorLifecycleStateLiteral = "ACTIVE"
    ttl_seconds: int = 86400  # Default 24h
    first_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_seen: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expiration: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 3: Threat Source Reliability
# ============================================================================

class ThreatSourceReliabilityDTO(BaseModel):
    source_id: str
    provider: str
    source_reliability_score: float = Field(default=0.85, ge=0.0, le=1.0)
    historical_accuracy: float = Field(default=0.90, ge=0.0, le=1.0)
    freshness_score: float = Field(default=0.95, ge=0.0, le=1.0)
    false_positive_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    is_authoritative: bool = False
    last_evaluated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 9 & 10: Threat Anomaly Detection
# ============================================================================

class ThreatAnomalyDTO(BaseModel):
    anomaly_id: str = Field(default_factory=lambda: f"anom_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    anomaly_type: str  # e.g., DOMAIN_BURST, INCIDENT_VELOCITY_SPIKE, INFRASTRUCTURE_ROTATION
    z_score: float
    observed_value: float
    baseline_mean: float
    baseline_std: float
    detection_method: str = "ROBUST_Z_SCORE"
    confidence: float = Field(default=0.90, ge=0.0, le=1.0)
    detected_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 5 & 6: Early Warning & Threat Propagation
# ============================================================================

class EarlyWarningDTO(BaseModel):
    warning_id: str = Field(default_factory=lambda: f"ew_{uuid.uuid4().hex[:12]}")
    tenant_id: str = "default_tenant"
    warning_type: str  # e.g., EMERGING_CAMPAIGN, RAPID_INFRASTRUCTURE_EXPANSION, CROSS_MODAL_CONVERGENCE
    severity: str = "HIGH"
    confidence: PredictionConfidenceLiteral = "HIGH"
    confidence_score: float = Field(default=0.85, ge=0.0, le=1.0)
    evidence_count: int = 1
    affected_entities: List[str] = Field(default_factory=list)
    propagation_score: float = Field(default=0.50, ge=0.0, le=1.0)
    time_horizon: str = "24H"
    current_risk_score: float = 65.0
    projected_risk_score: float = 88.0
    description: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 7 & 12: Campaign Growth & Forecasting
# ============================================================================

class CampaignForecastDTO(BaseModel):
    forecast_id: str = Field(default_factory=lambda: f"fcst_{uuid.uuid4().hex[:12]}")
    campaign_id: str
    growth_state: CampaignGrowthStateLiteral = "ACCELERATING"
    current_size: int = 1
    projected_growth_rate: float = 1.25
    current_risk: float = 75.0
    projected_risk: float = 90.0
    confidence: PredictionConfidenceLiteral = "MEDIUM"
    possible_next_events: List[str] = Field(default_factory=list)
    supporting_signals: List[str] = Field(default_factory=list)
    counter_evidence: List[str] = Field(default_factory=list)
    time_horizon: str = "72H"
    limitations: List[str] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 11: Predictive Risk
# ============================================================================

class PredictiveRiskDTO(BaseModel):
    entity_or_campaign_id: str
    current_observed_risk: float = Field(default=60.0, ge=0.0, le=100.0)
    projected_risk: float = Field(default=85.0, ge=0.0, le=100.0)
    prediction_confidence: float = Field(default=0.85, ge=0.0, le=1.0)
    risk_delta: float = 25.0
    time_horizon: str = "24H"
    supporting_factors: List[str] = Field(default_factory=list)
    counter_factors: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    calculated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 13, 14, 15: Threat Hunting
# ============================================================================

class ThreatHuntQueryDTO(BaseModel):
    query_type: str = "GRAPH_NEIGHBORS"  # DIRECT_INDICATOR, GRAPH_NEIGHBORS, INFRASTRUCTURE_REUSE, CERTIFICATE_SHARING
    search_term: str
    tenant_id: str = "default_tenant"
    max_depth: int = Field(default=2, ge=1, le=5)
    time_window_hours: int = 72


class ThreatHuntResultDTO(BaseModel):
    hunt_id: str = Field(default_factory=lambda: f"hunt_{uuid.uuid4().hex[:12]}")
    query: ThreatHuntQueryDTO
    results: List[Dict[str, Any]] = Field(default_factory=list)
    provenance_chain: List[str] = Field(default_factory=list)
    total_matched: int = 0
    executed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ============================================================================
# Section 20 & 21: Prediction Calibration & Outcomes
# ============================================================================

class PredictionCalibrationRecordDTO(BaseModel):
    prediction_id: str = Field(default_factory=lambda: f"pred_{uuid.uuid4().hex[:12]}")
    prediction_text: str
    predicted_probability: float = Field(ge=0.0, le=1.0)
    actual_outcome: Optional[str] = None  # OCCURRED, DID_NOT_OCCUR, INCONCLUSIVE
    brier_score_contribution: Optional[float] = None
    evaluated_at: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    model_config = ConfigDict(frozen=True, from_attributes=True)
