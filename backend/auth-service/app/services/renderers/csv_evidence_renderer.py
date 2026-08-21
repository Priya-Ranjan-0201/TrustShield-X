"""CSV Evidence Exporter (Phase 4.0 Part 3 — Sections 36-37).

Exports one row per canonical evidence reference with CSV formula injection protection.
"""

import csv
import io
from typing import Any, Optional, Dict
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.services.renderers.base_renderer import BaseReportRenderer


def _sanitize_csv_cell(value: Any) -> str:
    """Protect against CSV spreadsheet formula injection (Section 37).

    Any cell starting with '=', '+', '-', '@' is prefixed with a single quote.
    """
    if value is None:
        return ""
    val_str = str(value)
    if val_str and val_str[0] in ("=", "+", "-", "@"):
        return f"'{val_str}"
    return val_str


class CSVEvidenceRenderer(BaseReportRenderer):
    """Canonical CSV Evidence Exporter."""

    VERSION = "1.0.0"

    CSV_COLUMNS = [
        "report_id",
        "analysis_id",
        "finding_id",
        "evidence_id",
        "entity_id",
        "source_module",
        "evidence_type",
        "evidence_subtype",
        "confidence",
        "evidence_strength",
        "resolution_status",
        "relationship",
        "rule_id",
        "threat_match_id",
        "dataflow_id",
        "created_at",
    ]

    def validate_input(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
    ) -> bool:
        if not report_doc or not report_doc.report_id:
            return False
        return True

    def render(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        self.validate_input(report_doc, narrative_doc)

        output = io.StringIO()
        writer = csv.writer(output, lineterminator="\n")

        # Write header
        writer.writerow(self.CSV_COLUMNS)

        # Build mapping of finding_id to finding details
        finding_map = {}
        for f in report_doc.major_findings:
            finding_map[f.finding_id] = f

        # Export rows from evidence cards
        if report_doc.evidence_cards:
            for ev in report_doc.evidence_cards:
                fid = ev.finding_reference or ""
                matching_finding = finding_map.get(fid)
                rule_id = matching_finding.related_rules[0] if matching_finding and matching_finding.related_rules else ""
                threat_id = matching_finding.related_threat_matches[0] if matching_finding and matching_finding.related_threat_matches else ""
                entity_id = matching_finding.related_entities[0] if matching_finding and matching_finding.related_entities else ""

                row = [
                    _sanitize_csv_cell(report_doc.report_id),
                    _sanitize_csv_cell(report_doc.analysis_id),
                    _sanitize_csv_cell(fid),
                    _sanitize_csv_cell(ev.card_id),
                    _sanitize_csv_cell(entity_id),
                    _sanitize_csv_cell(ev.source),
                    _sanitize_csv_cell(ev.category),
                    _sanitize_csv_cell("OBSERVATION"),
                    _sanitize_csv_cell(ev.confidence),
                    _sanitize_csv_cell(ev.evidence_strength),
                    _sanitize_csv_cell("RESOLVED"),
                    _sanitize_csv_cell("SUPPORTS"),
                    _sanitize_csv_cell(rule_id),
                    _sanitize_csv_cell(threat_id),
                    _sanitize_csv_cell(""),
                    _sanitize_csv_cell(report_doc.generated_at),
                ]
                writer.writerow(row)
        else:
            # Fallback if no explicit evidence cards: emit rows from findings
            for f in report_doc.major_findings:
                row = [
                    _sanitize_csv_cell(report_doc.report_id),
                    _sanitize_csv_cell(report_doc.analysis_id),
                    _sanitize_csv_cell(f.finding_id),
                    _sanitize_csv_cell(f"ev_{f.finding_id}"),
                    _sanitize_csv_cell(f.related_entities[0] if f.related_entities else ""),
                    _sanitize_csv_cell(f.source_modules[0] if f.source_modules else "CoreEngine"),
                    _sanitize_csv_cell(f.category),
                    _sanitize_csv_cell("FINDING"),
                    _sanitize_csv_cell(f.confidence),
                    _sanitize_csv_cell(f.evidence_strength),
                    _sanitize_csv_cell("RESOLVED"),
                    _sanitize_csv_cell("SUPPORTS"),
                    _sanitize_csv_cell(f.related_rules[0] if f.related_rules else ""),
                    _sanitize_csv_cell(f.related_threat_matches[0] if f.related_threat_matches else ""),
                    _sanitize_csv_cell(""),
                    _sanitize_csv_cell(report_doc.generated_at),
                ]
                writer.writerow(row)

        return output.getvalue().encode("utf-8")

    def validate_output(self, rendered_bytes: bytes) -> bool:
        if not rendered_bytes or len(rendered_bytes) == 0:
            return False
        content = rendered_bytes.decode("utf-8", errors="ignore")
        first_line = content.splitlines()[0] if content.splitlines() else ""
        return "report_id" in first_line and "evidence_id" in first_line

    def get_content_type(self) -> str:
        return "text/csv; charset=utf-8"

    def get_file_extension(self) -> str:
        return "csv"

    def get_renderer_version(self) -> str:
        return self.VERSION
