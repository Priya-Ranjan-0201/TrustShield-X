"""Report Rendering Engine (Phase 4.0 Part 3 — Section 1).

Coordinates format renderers, manages format selection, validates outputs,
calculates hashes, and builds artifact DTOs.
"""

import time
from datetime import datetime, timezone
from typing import Any, Optional, Dict, Tuple
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.schemas.report_rendering_models import ReportArtifactDTO
from app.services.renderers.base_renderer import BaseReportRenderer
from app.services.renderers.json_report_renderer import JSONReportRenderer
from app.services.renderers.html_report_renderer import HTMLReportRenderer
from app.services.renderers.pdf_report_renderer import PDFReportRenderer
from app.services.renderers.markdown_report_renderer import MarkdownReportRenderer
from app.services.renderers.csv_evidence_renderer import CSVEvidenceRenderer


class ReportRenderingEngine:
    """Master Rendering Engine dispatching to format-specific renderers."""

    def __init__(self):
        self.renderers: Dict[str, BaseReportRenderer] = {
            "JSON": JSONReportRenderer(),
            "HTML": HTMLReportRenderer(),
            "PDF": PDFReportRenderer(),
            "MARKDOWN": MarkdownReportRenderer(),
            "MD": MarkdownReportRenderer(),
            "CSV": CSVEvidenceRenderer(),
        }

    def get_renderer(self, format_name: str) -> BaseReportRenderer:
        fmt = (format_name or "JSON").upper()
        if fmt not in self.renderers:
            raise ValueError(f"TSX-REPORT-606: Unsupported rendering format '{format_name}'.")
        return self.renderers[fmt]

    def render_artifact(
        self,
        report_doc: ReportDocumentDTO,
        narrative_doc: Optional[NarrativeDocumentDTO] = None,
        format_name: str = "JSON",
        options: Optional[Dict[str, Any]] = None,
    ) -> Tuple[ReportArtifactDTO, bytes]:
        """Render a report document into the specified format and return artifact metadata & bytes."""
        start_time = time.time()
        fmt = (format_name or "JSON").upper()
        renderer = self.get_renderer(fmt)

        # Validate input
        if not renderer.validate_input(report_doc, narrative_doc):
            raise ValueError(f"TSX-REPORT-600: Invalid report input for format '{fmt}'.")

        # Perform rendering
        rendered_bytes = renderer.render(report_doc, narrative_doc, options)

        # Validate rendered output
        if not renderer.validate_output(rendered_bytes):
            raise ValueError(f"TSX-REPORT-600: Render validation failed for format '{fmt}'.")

        duration_ms = (time.time() - start_time) * 1000
        size_bytes = renderer.calculate_size(rendered_bytes)
        sha256_hash = renderer.calculate_hash(rendered_bytes)

        now_str = datetime.now(timezone.utc).isoformat()
        artifact_id = f"art_{report_doc.report_id}_{fmt.lower()}"

        artifact_dto = ReportArtifactDTO(
            artifact_id=artifact_id,
            report_id=report_doc.report_id,
            analysis_id=report_doc.analysis_id,
            report_version=report_doc.report_version,
            artifact_version="1.0.0",
            format=fmt,
            mime_type=renderer.get_content_type(),
            file_extension=renderer.get_file_extension(),
            size_bytes=size_bytes,
            sha256=sha256_hash,
            content_encoding="utf-8" if fmt != "PDF" else "binary",
            renderer_name=renderer.__class__.__name__,
            renderer_version=renderer.get_renderer_version(),
            schema_version=report_doc.schema_version,
            generated_at=now_str,
            generation_duration_ms=duration_ms,
            storage_location=f"artifacts/{artifact_id}.{renderer.get_file_extension()}",
            status="COMPLETED",
            created_at=now_str,
        )

        return artifact_dto, rendered_bytes
