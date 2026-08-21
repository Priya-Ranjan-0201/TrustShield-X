"""Master Document Trust Detector Engine.

Orchestrates the full document verification pipeline:
  Image Preprocessing → OCR → Classification → Field Extraction →
  Forgery Detection → Template Validation → Image Quality Analysis →
  Evidence Aggregation → Risk Score → Confidence → Result

Score computation (from Design.md Section 4):
  Base = 100
  For each evidence finding:
    CRITICAL → deduct 40 pts
    HIGH     → deduct 25 pts
    MEDIUM   → deduct 10 pts
    LOW      → deduct 3 pts
  risk_score = sum of deductions, capped at 100, floored at 0
  trust_score = max(0, 100 - risk_score)

Unknown document handling:
  Classified as UNKNOWN → skip document-specific field extraction and government
  validation, still run generic image-tampering analysis. Verdict caps at
  MEDIUM RISK maximum (risk_score ≤ 50) with explicit evidence note.

Confidence is OCR engine's own reported confidence — kept separate from risk score.
"""

import time
from typing import Dict, Any, List

from app.services.ocr_engine import OCROrchestrator, OCRResult
from app.services.document_classifier import classify_document
from app.services.document_field_extractor import extract_fields_for_document
from app.services.document_forgery_detector import run_forgery_detection
from app.services.document_format_validator import validate_document_format
from app.services.image_quality_analyzer import analyze_image_quality, generate_quality_evidence


# Severity deduction weights (Design.md Section 4 trust score matrix)
SEVERITY_DEDUCTIONS = {
    "CRITICAL": 40,
    "HIGH": 25,
    "MEDIUM": 10,
    "LOW": 3,
    "INFO": 0,
}


class DocumentDetectorResult:
    def __init__(
        self,
        module: str,
        status: str,
        document_type: str,
        classification_confidence: float,
        extracted_fields: Dict[str, Any],
        ocr_confidence: float,
        ocr_engine_used: str,
        image_quality_metrics: Dict[str, Any],
        risk_score: int,
        confidence_score: float,
        severity: str,
        evidence: List[Dict[str, str]],
        recommendations: List[str],
        disclaimer: str,
        masking_note: str,
        execution_time_ms: int,
    ):
        self.module = module
        self.status = status
        self.document_type = document_type
        self.classification_confidence = classification_confidence
        self.extracted_fields = extracted_fields
        self.ocr_confidence = ocr_confidence
        self.ocr_engine_used = ocr_engine_used
        self.image_quality_metrics = image_quality_metrics
        self.risk_score = risk_score
        self.confidence_score = confidence_score
        self.severity = severity
        self.evidence = evidence
        self.recommendations = recommendations
        self.disclaimer = disclaimer
        self.masking_note = masking_note
        self.execution_time_ms = execution_time_ms

    def to_dict(self) -> Dict[str, Any]:
        return {
            "module": self.module,
            "status": self.status,
            "document_type": self.document_type,
            "classification_confidence": self.classification_confidence,
            "extracted_fields": self.extracted_fields,
            "ocr_confidence": self.ocr_confidence,
            "ocr_engine_used": self.ocr_engine_used,
            "image_quality_metrics": self.image_quality_metrics,
            "risk_score": self.risk_score,
            "confidence_score": self.confidence_score,
            "severity": self.severity,
            "evidence": self.evidence,
            "recommendations": self.recommendations,
            "disclaimer": self.disclaimer,
            "masking_note": self.masking_note,
            "execution_time_ms": self.execution_time_ms,
        }


def _compute_risk_score(evidence: List[Dict[str, str]]) -> int:
    """Computes risk score from evidence using weighted deduction model.

    Formula (documented per Design.md Section 4):
      risk_score = sum of severity deductions for each evidence finding
      CRITICAL = 40 pts, HIGH = 25 pts, MEDIUM = 10 pts, LOW = 3 pts
      Capped at 100, floored at 0.

    Worked example:
      - Missing hologram region → MEDIUM (10 pts)
      - Font inconsistency → HIGH (25 pts)
      - Low resolution → LOW (3 pts)
      risk_score = 10 + 25 + 3 = 38
      trust_score = 100 - 38 = 62 → MEDIUM RISK
    """
    total_deduction = 0
    for item in evidence:
        sev = item.get("severity", "INFO").upper()
        total_deduction += SEVERITY_DEDUCTIONS.get(sev, 0)
    return min(100, max(0, total_deduction))


def _severity_from_trust_score(trust_score: int) -> str:
    """Maps trust score to severity tier per Design.md Section 4.

    90-100 → TRUSTED
    70-89  → LOW RISK
    50-69  → MEDIUM RISK
    30-49  → HIGH RISK
    0-29   → DANGEROUS
    """
    if trust_score >= 90:
        return "TRUSTED"
    elif trust_score >= 70:
        return "LOW RISK"
    elif trust_score >= 50:
        return "MEDIUM RISK"
    elif trust_score >= 30:
        return "HIGH RISK"
    else:
        return "DANGEROUS"


class DocumentTrustDetector:
    def __init__(self):
        self.ocr = OCROrchestrator()

    async def analyze_document(
        self, file_bytes: bytes, filename: str | None = None
    ) -> DocumentDetectorResult:
        """Runs the full document trust verification pipeline."""
        start_time = time.time()

        all_evidence: List[Dict[str, str]] = []
        recommendations: List[str] = []

        # 1. OCR Extraction
        try:
            ocr_result = await self.ocr.extract_text(file_bytes)
        except RuntimeError as e:
            error_msg = str(e)
            execution_time_ms = int((time.time() - start_time) * 1000)
            return DocumentDetectorResult(
                module="document-trust",
                status="failed",
                document_type="UNKNOWN",
                classification_confidence=0.0,
                extracted_fields={},
                ocr_confidence=0.0,
                ocr_engine_used="none",
                image_quality_metrics={},
                risk_score=100,
                confidence_score=0.0,
                severity="DANGEROUS",
                evidence=[{
                    "type": "OCR_ERROR",
                    "severity": "CRITICAL",
                    "title": "OCR Processing Failed",
                    "description": error_msg,
                }],
                recommendations=["Re-upload a clearer, higher-resolution scan of the document."],
                disclaimer="Unable to analyze document — OCR extraction failed.",
                masking_note="",
                execution_time_ms=execution_time_ms,
            )

        # 2. Document Classification
        document_type, classification_confidence = classify_document(ocr_result.text)

        # 3. Field Extraction (masked per DPDP compliance)
        if document_type != "UNKNOWN":
            extracted_fields = extract_fields_for_document(document_type, ocr_result.text)
        else:
            extracted_fields = {
                "document_type": "UNKNOWN",
                "note": "Document type could not be determined — field extraction skipped.",
            }

        # 4. Forgery Detection (named heuristics)
        forgery_evidence = run_forgery_detection(file_bytes, ocr_result, document_type)
        all_evidence.extend(forgery_evidence)

        # 5. Government Format Validation (if applicable)
        if document_type != "UNKNOWN":
            format_evidence, disclaimer = validate_document_format(document_type, ocr_result.text)
            all_evidence.extend(format_evidence)
        else:
            disclaimer = (
                "Document type could not be verified — treat with caution. "
                "This validates structure and internal consistency only — it does NOT "
                "confirm authenticity against any government database."
            )
            all_evidence.append({
                "type": "CLASSIFICATION",
                "severity": "MEDIUM",
                "title": "Unrecognized Document Type",
                "description": (
                    "The document could not be classified into any known type. "
                    "Document-specific field extraction and government format validation "
                    "were skipped. Treat this document with caution."
                ),
            })

        # 6. Image Quality Analysis
        quality_metrics = analyze_image_quality(file_bytes)
        quality_evidence = generate_quality_evidence(quality_metrics)
        all_evidence.extend(quality_evidence)

        # 7. Risk Score Computation (weighted evidence model)
        risk_score = _compute_risk_score(all_evidence)

        # 8. Unknown Document Verdict Cap (MEDIUM RISK maximum)
        if document_type == "UNKNOWN" and risk_score < 50:
            risk_score = 50  # Cap: never auto-Trusted for Unknown

        trust_score = max(0, 100 - risk_score)
        severity = _severity_from_trust_score(trust_score)

        # 9. Confidence Score (OCR engine's own confidence, separate from risk)
        confidence_score = ocr_result.confidence

        # 10. Recommendations
        if document_type == "UNKNOWN":
            recommendations.append(
                "Document type could not be verified. If this is an official document, "
                "consider obtaining a certified copy from the issuing authority."
            )

        if risk_score >= 50:
            recommendations.append(
                "This document shows signs that warrant manual verification. "
                "Cross-check with the issuing authority before relying on it."
            )

        if any(e.get("severity") == "CRITICAL" for e in all_evidence):
            recommendations.append(
                "Critical forgery indicators detected. Do NOT accept this document "
                "as proof of identity or authority without independent verification."
            )

        if not recommendations:
            recommendations.append(
                "Document appears structurally consistent. Standard verification practices apply."
            )

        # Masking compliance note
        masking_note = (
            "Sensitive identifiers are masked per DPDP Act 2023 / UIDAI compliance. "
            "Aadhaar: only last 4 digits stored. PAN/Passport/Licence: masked in storage and logs. "
            "Full values are shown only to the uploading user in the frontend result view."
        )

        execution_time_ms = int((time.time() - start_time) * 1000)

        return DocumentDetectorResult(
            module="document-trust",
            status="completed",
            document_type=document_type,
            classification_confidence=classification_confidence,
            extracted_fields=extracted_fields,
            ocr_confidence=ocr_result.confidence,
            ocr_engine_used=ocr_result.engine_used,
            image_quality_metrics=quality_metrics,
            risk_score=risk_score,
            confidence_score=confidence_score,
            severity=severity,
            evidence=all_evidence,
            recommendations=recommendations,
            disclaimer=disclaimer,
            masking_note=masking_note,
            execution_time_ms=execution_time_ms,
        )
