"""Pydantic v2 DTO Schemas for Automated Digital Trust Report Generator (Phase 4.0 Part 1).

Strictly typed DTOs for reports, sections, findings, evidence cards, threat intelligence,
provenance, lineage, versions, runs, errors, telemetry, and metrics.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class TrustOverviewDTO(BaseModel):
    risk_score: float = 0.0
    risk_band: str = "TRUSTED"
    confidence: str = "HIGH"
    evidence_sufficiency: str = "SUFFICIENT"
    analysis_status: str = "COMPLETED"
    modules_analyzed: List[str] = Field(default_factory=list)
    findings_count: int = 0
    evidence_count: int = 0
    threat_matches: int = 0
    critical_findings: int = 0
    high_risk_findings: int = 0
    contradictions: int = 0
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportFindingDTO(BaseModel):
    finding_id: str
    category: str
    title: str
    description: str
    status: str = "CONFIRMED"
    confidence: str = "HIGH"
    severity_reference: str = "MEDIUM"
    evidence_strength: str = "STRONG"
    source_modules: List[str] = Field(default_factory=list)
    evidence_count: int = 1
    independent_source_count: int = 1
    related_entities: List[str] = Field(default_factory=list)
    related_rules: List[str] = Field(default_factory=list)
    related_threat_matches: List[str] = Field(default_factory=list)
    provenance_reference: str = "prov_ref_default"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportEvidenceCardDTO(BaseModel):
    card_id: str
    title: str
    category: str
    observation: str
    evidence_strength: str = "STRONG"
    confidence: str = "HIGH"
    source: str = "CoreEngine"
    provenance: str = "prov_default"
    finding_reference: str = ""
    limitations: List[str] = Field(default_factory=list)


    model_config = ConfigDict(frozen=True, from_attributes=True)


class ContradictionReportSectionDTO(BaseModel):
    contradiction_id: str
    finding: str
    evidence_a: str
    evidence_b: str
    source_a: str
    source_b: str
    confidence_a: str
    confidence_b: str
    explanation: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportProvenanceDTO(BaseModel):
    statement_id: str
    source_module: str
    finding_id: str
    evidence_id: str
    timestamp: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportLineageDTO(BaseModel):
    section_id: str
    statement_text: str
    finding_id: str
    evidence_id: str
    original_source: str

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportDocumentDTO(BaseModel):
    report_id: str
    analysis_id: str
    report_version: str = "1.0.0"
    schema_version: str = "4.0.0"
    generated_at: str
    generated_by: str = "TruthShield Report Generator Engine"
    report_type: str = "FULL_TRUST_REPORT"
    status: str = "COMPLETED"
    language: str = "en"
    format: str = "JSON"
    trust_overview: TrustOverviewDTO
    risk_assessment: Dict[str, Any] = Field(default_factory=dict)
    executive_summary: Dict[str, Any] = Field(default_factory=dict)
    major_findings: List[ReportFindingDTO] = Field(default_factory=list)
    evidence_cards: List[ReportEvidenceCardDTO] = Field(default_factory=list)
    threat_intelligence: List[Dict[str, Any]] = Field(default_factory=list)
    behavior_analysis: List[Dict[str, Any]] = Field(default_factory=list)
    dataflow_analysis: List[Dict[str, Any]] = Field(default_factory=list)
    module_results: Dict[str, Any] = Field(default_factory=dict)
    mitigations: List[str] = Field(default_factory=list)
    protective_factors: List[str] = Field(default_factory=list)
    contradictions: List[ContradictionReportSectionDTO] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    technical_details: Dict[str, Any] = Field(default_factory=dict)
    provenance: List[ReportProvenanceDTO] = Field(default_factory=list)
    lineage: List[ReportLineageDTO] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True, from_attributes=True)


class DigitalTrustReportDTO(BaseModel):
    report_id: str
    analysis_id: str
    report_version: str = "1.0.0"
    schema_version: str = "4.0.0"
    status: str = "COMPLETED"
    created_at: str
    document: ReportDocumentDTO

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportVersionDTO(BaseModel):
    report_id: str
    report_version: str = "1.0.0"
    created_at: str
    change_reason: str = "INITIAL_GENERATION"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportGenerationRunDTO(BaseModel):
    run_id: str
    analysis_id: str
    report_id: str
    duration_ms: int = 0
    status: str = "SUCCESS"

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportMetricDTO(BaseModel):
    reports_generated_total: int = 1
    reports_failed_total: int = 0
    generation_duration_ms: float = 0.0

    model_config = ConfigDict(frozen=True, from_attributes=True)
