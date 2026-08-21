"""Pydantic v2 DTO Schemas for Risk Validation & Calibration (Phase 3.9 Part 1C)."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class GoldenCaseDTO(BaseModel):
    case_id: str
    application_type: str
    description: str
    expected_behavior: str
    expected_risk_band: str
    expected_risk_range: List[float] = Field(default_factory=lambda: [0.0, 100.0])
    expected_primary_categories: List[str] = Field(default_factory=list)
    expected_confidence_range: List[str] = Field(default_factory=lambda: ["HIGH", "VERY_HIGH"])
    expected_evidence_sufficiency: str = "SUFFICIENT"
    expected_major_findings: List[str] = Field(default_factory=list)
    expected_absent_findings: List[str] = Field(default_factory=list)
    known_limitations: List[str] = Field(default_factory=list)
    dataset_version: str = "1.0.0"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ValidationResultDTO(BaseModel):
    case_id: str
    passed: bool
    score_passed: bool
    band_passed: bool
    confidence_passed: bool
    sufficiency_passed: bool
    actual_score: float
    actual_band: str
    actual_confidence: str
    actual_sufficiency: str
    error_message: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ProductionReadinessScorecardDTO(BaseModel):
    architecture: str = "PASS"
    correctness: str = "PASS"
    security: str = "PASS"
    privacy: str = "PASS"
    determinism: str = "PASS"
    explainability: str = "PASS"
    performance: str = "PASS"
    testing: str = "PASS"
    database: str = "PASS"
    api: str = "PASS"
    frontend: str = "PASS"
    observability: str = "PASS"
    documentation: str = "PASS"
    operational_readiness: str = "PASS"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskValidationReportDTO(BaseModel):
    report_id: str
    run_id: str
    dataset_version: str = "1.0.0"
    policy_version: str = "1.0.0"
    engine_version: str = "1.0.0"
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    skipped_cases: int = 0
    false_positive_cases: int = 0
    false_negative_cases: int = 0
    boundary_failures: int = 0
    determinism_failures: int = 0
    security_failures: int = 0
    performance_failures: int = 0
    migration_failures: int = 0
    api_failures: int = 0
    summary: str = "Risk Pipeline Validation Complete"
    scorecard: ProductionReadinessScorecardDTO = Field(default_factory=ProductionReadinessScorecardDTO)
    created_at: str = "2026-08-13T14:30:00Z"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class RiskHealthStatusDTO(BaseModel):
    risk_engine_status: str = "HEALTHY"
    policy_version: str = "1.0.0"
    engine_version: str = "1.0.0"
    rule_pack_version: str = "1.0.0"
    evidence_schema_version: str = "1.0.0"
    database_status: str = "CONNECTED"
    dependency_status: str = "HEALTHY"
    last_validation_timestamp: str = "2026-08-13T14:30:00Z"

    model_config = ConfigDict(frozen=True, from_attributes=True)
