"""Pydantic v2 DTO Schemas for Digital Trust Report Rendering, Export & Delivery Engine (Phase 4.0 Part 3).

Strictly typed DTOs for artifacts, export jobs, digital signatures, integrity records,
manifests, storage records, rendering runs, rendering errors, format validations,
download audits, comparisons, and export requests.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Section 5-6: Report Artifact DTO
# ---------------------------------------------------------------------------

class ReportArtifactDTO(BaseModel):
    """Metadata describing a rendered report artifact."""
    artifact_id: str
    report_id: str
    analysis_id: str
    report_version: str = "1.0.0"
    artifact_version: str = "1.0.0"
    format: str = "JSON"  # JSON, HTML, PDF, MARKDOWN, CSV
    mime_type: str = "application/json"
    file_extension: str = "json"
    size_bytes: int = 0
    sha256: str = ""
    content_encoding: str = "utf-8"
    renderer_name: str = "JSONReportRenderer"
    renderer_version: str = "1.0.0"
    schema_version: str = "4.0.0"
    generated_at: str = ""
    generation_duration_ms: float = 0.0
    storage_location: str = ""
    status: str = "COMPLETED"  # GENERATING, COMPLETED, FAILED, CORRUPTED, EXPIRED, REVOKED, DELETED, ARCHIVED
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 63: Export Job DTO
# ---------------------------------------------------------------------------

class ReportExportJobDTO(BaseModel):
    """Represents an asynchronous or scheduled export job."""
    job_id: str
    report_id: str
    format: str = "PDF"
    status: str = "COMPLETED"  # PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    progress: int = 100
    requested_by: str = "system"
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    artifact_id: Optional[str] = None
    error_code: Optional[str] = None

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 41-42: Digital Signature DTO
# ---------------------------------------------------------------------------

class ReportSignatureDTO(BaseModel):
    """Cryptographic signature record for a report artifact."""
    signature_id: str
    artifact_id: str
    algorithm: str = "Ed25519"  # Ed25519, ECDSA, RSA-PSS
    key_id: str = ""
    signature: str = ""
    signed_hash: str = ""
    signed_at: str = ""
    status: str = "NOT_SIGNED"  # NOT_SIGNED, SIGNED, VERIFIED, INVALID, REVOKED

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 39 & 56: Integrity Record DTO
# ---------------------------------------------------------------------------

class ReportIntegrityRecordDTO(BaseModel):
    """Record verifying logical content and artifact binary integrity."""
    integrity_id: str
    report_id: str
    artifact_id: str
    content_hash: str
    artifact_hash: str
    is_valid: bool = True
    verified_at: str = ""
    detected_tampering: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 40: Report Manifest DTO
# ---------------------------------------------------------------------------

class ReportManifestDTO(BaseModel):
    """Machine-readable manifest summarizing report generation lineage."""
    report_id: str
    analysis_id: str
    report_version: str = "1.0.0"
    artifact_id: str
    artifact_format: str = "JSON"
    artifact_sha256: str
    content_sha256: str
    report_schema_version: str = "4.0.0"
    narrative_version: str = "1.0.0"
    renderer_version: str = "1.0.0"
    risk_policy_version: str = "1.0.0"
    engine_versions: Dict[str, str] = Field(default_factory=dict)
    generated_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 48-49: Artifact Storage Record DTO
# ---------------------------------------------------------------------------

class ArtifactStorageRecordDTO(BaseModel):
    """Storage location and provider record."""
    storage_id: str
    artifact_id: str
    provider: str = "LOCAL"  # LOCAL, S3, AZURE, GCP
    bucket_or_path: str = ""
    object_key: str = ""
    size_bytes: int = 0
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 67-68: Telemetry & Metrics DTOs
# ---------------------------------------------------------------------------

class ReportRenderingRunDTO(BaseModel):
    run_id: str
    report_id: str
    artifact_id: str
    format: str
    duration_ms: float = 0.0
    status: str = "SUCCESS"
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportRenderingErrorDTO(BaseModel):
    error_id: str
    report_id: str
    error_code: str = "TSX-REPORT-600"
    error_message: str
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportFormatValidationDTO(BaseModel):
    validation_id: str
    report_id: str
    formats_tested: List[str] = Field(default_factory=list)
    consistent: bool = True
    discrepancies: List[str] = Field(default_factory=list)
    created_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportDownloadAuditDTO(BaseModel):
    audit_id: str
    artifact_id: str
    user_id: str
    ip_address: str = "127.0.0.1"
    downloaded_at: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


# ---------------------------------------------------------------------------
# Section 43 & 79: Comparison and Verification Response DTOs
# ---------------------------------------------------------------------------

class ReportComparisonDTO(BaseModel):
    report_id_a: str
    report_id_b: str
    risk_score_delta: float = 0.0
    risk_band_changed: bool = False
    risk_band_a: str = ""
    risk_band_b: str = ""
    confidence_a: str = ""
    confidence_b: str = ""
    findings_added: List[str] = Field(default_factory=list)
    findings_removed: List[str] = Field(default_factory=list)
    evidence_count_delta: int = 0
    recommendations_changed: bool = False
    policy_version_changed: bool = False
    engine_version_changed: bool = False
    report_version_changed: bool = False

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportVerificationResponseDTO(BaseModel):
    report_id: str
    artifact_id: str
    artifact_integrity: bool = True
    content_integrity: bool = True
    sha256: str = ""
    content_hash: str = ""
    signature_status: str = "NOT_SIGNED"
    signature_algorithm: Optional[str] = None
    report_version: str = "1.0.0"
    renderer_version: str = "1.0.0"
    schema_version: str = "4.0.0"
    verification_timestamp: str = ""

    model_config = ConfigDict(frozen=True, from_attributes=True)


class ReportExportRequestDTO(BaseModel):
    format: str = "PDF"  # JSON, HTML, PDF, MARKDOWN, CSV
    language: str = "en"
    include_appendix: bool = True
    include_provenance: bool = True
    include_evidence: bool = True
    watermark: Optional[str] = None  # CONFIDENTIAL, INTERNAL, DRAFT, UNVERIFIED, ARCHIVED

    model_config = ConfigDict(frozen=True, from_attributes=True)
