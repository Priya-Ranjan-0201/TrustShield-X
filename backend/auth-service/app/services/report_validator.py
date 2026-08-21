"""Report Validator Service (Phase 4.0 Part 1).

Enforces critical consistency rules:
- Report Risk Score == Authoritative Risk Assessment Score
- Report Risk Band == Authoritative Risk Assessment Band
- Report Confidence == Authoritative Risk Confidence
- Report Evidence Sufficiency == Authoritative Evidence Sufficiency
Mismatch triggers ValueError ("REPORT_GENERATION_ERROR").
"""

from typing import Any
from app.schemas.digital_trust_report_models import ReportDocumentDTO


class ReportValidator:
    """Validator ensuring report data consistency and risk integrity."""

    def validate_report(self, doc: ReportDocumentDTO, risk_assessment_dto: Any = None) -> bool:
        if not risk_assessment_dto:
            return True

        expected_score = getattr(risk_assessment_dto, "risk_score", doc.trust_overview.risk_score)
        expected_band = getattr(risk_assessment_dto, "risk_band", doc.trust_overview.risk_band)
        expected_conf = getattr(risk_assessment_dto, "confidence_level", doc.trust_overview.confidence)
        expected_suff = getattr(risk_assessment_dto, "evidence_sufficiency", doc.trust_overview.evidence_sufficiency)

        if doc.trust_overview.risk_score != expected_score:
            raise ValueError(f"REPORT_GENERATION_ERROR: Risk score mismatch ({doc.trust_overview.risk_score} vs {expected_score})")

        if doc.trust_overview.risk_band != expected_band:
            raise ValueError(f"REPORT_GENERATION_ERROR: Risk band mismatch ({doc.trust_overview.risk_band} vs {expected_band})")

        if doc.trust_overview.confidence != expected_conf:
            raise ValueError(f"REPORT_GENERATION_ERROR: Confidence mismatch ({doc.trust_overview.confidence} vs {expected_conf})")

        if doc.trust_overview.evidence_sufficiency != expected_suff:
            raise ValueError(f"REPORT_GENERATION_ERROR: Evidence sufficiency mismatch ({doc.trust_overview.evidence_sufficiency} vs {expected_suff})")

        return True
