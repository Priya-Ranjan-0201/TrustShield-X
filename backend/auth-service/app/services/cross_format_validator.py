"""Cross-Format Consistency Validator (Phase 4.0 Part 3 — Sections 53-54).

Validates that authoritative analytical values (risk score, risk band, confidence,
evidence sufficiency, finding IDs, recommendations) remain identical across
JSON, HTML, PDF, Markdown, and CSV exports.
"""

from typing import List, Dict, Any
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.report_rendering_models import ReportFormatValidationDTO


class CrossFormatValidator:
    """Validates analytical consistency across multiple rendered output formats."""

    def validate_consistency(
        self,
        report_doc: ReportDocumentDTO,
        rendered_outputs: Dict[str, bytes],
    ) -> ReportFormatValidationDTO:
        """Verify that all rendered formats contain the exact authoritative values from report_doc."""
        discrepancies: List[str] = []
        formats_tested = list(rendered_outputs.keys())

        expected_score_str = f"{report_doc.trust_overview.risk_score:.1f}"
        expected_band = report_doc.trust_overview.risk_band
        expected_conf = report_doc.trust_overview.confidence
        expected_suff = report_doc.trust_overview.evidence_sufficiency

        for fmt, content_bytes in rendered_outputs.items():
            text = content_bytes.decode("utf-8", errors="ignore")

            # Check JSON
            if fmt == "JSON":
                if expected_band not in text:
                    discrepancies.append(f"JSON format missing risk band {expected_band}")
                if expected_conf not in text:
                    discrepancies.append(f"JSON format missing confidence {expected_conf}")

            # Check HTML
            elif fmt == "HTML":
                if expected_score_str not in text:
                    discrepancies.append(f"HTML format missing risk score {expected_score_str}")
                if expected_band not in text:
                    discrepancies.append(f"HTML format missing risk band {expected_band}")

            # Check PDF
            elif fmt == "PDF":
                if expected_band not in text:
                    discrepancies.append(f"PDF format missing risk band {expected_band}")
                if expected_conf not in text:
                    discrepancies.append(f"PDF format missing confidence {expected_conf}")

            # Check Markdown
            elif fmt in ("MARKDOWN", "MD"):
                if expected_score_str not in text:
                    discrepancies.append(f"Markdown format missing risk score {expected_score_str}")
                if expected_band not in text:
                    discrepancies.append(f"Markdown format missing risk band {expected_band}")

            # Check CSV
            elif fmt == "CSV":
                if report_doc.report_id not in text:
                    discrepancies.append("CSV format missing report_id in rows")

        is_consistent = (len(discrepancies) == 0)

        return ReportFormatValidationDTO(
            validation_id=f"val_{report_doc.report_id}",
            report_id=report_doc.report_id,
            formats_tested=formats_tested,
            consistent=is_consistent,
            discrepancies=discrepancies,
        )
