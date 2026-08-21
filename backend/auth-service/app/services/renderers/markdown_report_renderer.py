"""Markdown Report Renderer (Phase 4.0 Part 3 — Section 35).

Generates clean, GitHub-flavored Markdown reports with structured headings,
tables, provenance links, and technical details.
"""

from typing import Any, Optional, Dict
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.services.renderers.base_renderer import BaseReportRenderer


class MarkdownReportRenderer(BaseReportRenderer):
    """Markdown Report Renderer generating README-style reports."""

    VERSION = "1.0.0"

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

        ov = report_doc.trust_overview
        risk_score = ov.risk_score
        risk_band = ov.risk_band
        confidence = ov.confidence
        sufficiency = ov.evidence_sufficiency
        watermark = (options or {}).get("watermark", "")

        md_lines = []

        if watermark:
            md_lines.append(f"> **[{watermark.upper()}]**\n")

        md_lines.extend([
            f"# Digital Trust Report",
            f"",
            f"**Report ID:** `{report_doc.report_id}` | **Analysis ID:** `{report_doc.analysis_id}` | **Generated At:** {report_doc.generated_at}",
            f"",
            f"---",
            f"",
            f"## Executive Summary",
            f"",
        ])

        if narrative_doc and narrative_doc.executive_summary:
            es = narrative_doc.executive_summary
            md_lines.append(f"### {es.headline}")
            md_lines.append(f"")
            md_lines.append(f"{es.overall_assessment}")
            md_lines.append(f"")
            md_lines.append(f"**Recommended Action:** {es.recommended_action}")
        else:
            md_lines.append(f"The analysis concluded with risk band **{risk_band}** and risk score **{risk_score:.1f}/100**.")

        md_lines.extend([
            f"",
            f"---",
            f"",
            f"## Risk Assessment",
            f"",
            f"| Metric | Value |",
            f"| :--- | :--- |",
            f"| **Risk Score** | **{risk_score:.1f} / 100** |",
            f"| **Risk Band** | **{risk_band}** |",
            f"| **Confidence** | {confidence} |",
            f"| **Evidence Sufficiency** | {sufficiency} |",
            f"| **Findings Count** | {ov.findings_count} |",
            f"| **Evidence Count** | {ov.evidence_count} |",
            f"| **Threat Matches** | {ov.threat_matches} |",
            f"| **Contradictions** | {ov.contradictions} |",
            f"",
            f"---",
            f"",
            f"## Findings",
            f"",
        ])

        if report_doc.major_findings:
            for f in report_doc.major_findings:
                md_lines.append(f"### Finding [{f.finding_id}]: {f.title}")
                md_lines.append(f"")
                md_lines.append(f"- **Category:** `{f.category}`")
                md_lines.append(f"- **Confidence:** `{f.confidence}`")
                md_lines.append(f"- **Evidence Strength:** `{f.evidence_strength}`")
                md_lines.append(f"- **Description:** {f.description}")
                if f.source_modules:
                    md_lines.append(f"- **Source Modules:** {', '.join(f.source_modules)}")
                if f.provenance_reference:
                    md_lines.append(f"- **Provenance Reference:** [`{f.provenance_reference}`](#provenance)")
                md_lines.append(f"")
        else:
            md_lines.append("No major security findings identified.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Evidence",
            f"",
        ])

        if report_doc.evidence_cards:
            for ev in report_doc.evidence_cards:
                md_lines.append(f"#### Evidence [{ev.card_id}]: {ev.title}")
                md_lines.append(f"- **Category:** `{ev.category}` | **Strength:** `{ev.evidence_strength}` | **Source:** `{ev.source}`")
                md_lines.append(f"- **Observation:** {ev.observation}")
                if ev.limitations:
                    md_lines.append(f"- **Limitations:** {'; '.join(ev.limitations)}")
                md_lines.append(f"")
        else:
            md_lines.append("No evidence cards recorded.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Threat Intelligence",
            f"",
        ])

        if report_doc.threat_intelligence:
            md_lines.append("| Indicator | Type | Provider | Confidence | Freshness |")
            md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for ti in report_doc.threat_intelligence:
                ind = ti.get("indicator", "N/A")
                t_type = ti.get("type", ti.get("ioc_type", "N/A"))
                prov = ti.get("provider", "Internal")
                conf = ti.get("confidence", "HIGH")
                fresh = ti.get("freshness", "CURRENT")
                md_lines.append(f"| `{ind}` | {t_type} | {prov} | {conf} | {fresh} |")
            md_lines.append("")
        else:
            md_lines.append("No threat intelligence matches observed.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Recommendations",
            f"",
        ])

        if report_doc.recommendations:
            for i, rec in enumerate(report_doc.recommendations, 1):
                md_lines.append(f"{i}. {rec}")
            md_lines.append("")
        else:
            md_lines.append("No specific recommendations at this time.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Limitations",
            f"",
        ])

        if report_doc.limitations:
            for lim in report_doc.limitations:
                md_lines.append(f"- {lim}")
            md_lines.append("")
        else:
            md_lines.append("- Standard static analysis limitations apply.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Provenance",
            f"",
        ])

        if report_doc.provenance:
            md_lines.append("| Statement ID | Source Module | Finding ID | Evidence ID | Timestamp |")
            md_lines.append("| :--- | :--- | :--- | :--- | :--- |")
            for p in report_doc.provenance:
                md_lines.append(f"| `{p.statement_id}` | `{p.source_module}` | `{p.finding_id}` | `{p.evidence_id}` | `{p.timestamp}` |")
            md_lines.append("")
        else:
            md_lines.append("No provenance records recorded.")
            md_lines.append("")

        md_lines.extend([
            f"---",
            f"",
            f"## Technical Appendix",
            f"",
            f"- **Report Schema Version:** `{report_doc.schema_version}`",
            f"- **Report Document Version:** `{report_doc.report_version}`",
            f"- **Renderer:** `MarkdownReportRenderer v{self.VERSION}`",
            f"- **Generated By:** `{report_doc.generated_by}`",
            f"",
        ])

        return "\n".join(md_lines).encode("utf-8")

    def validate_output(self, rendered_bytes: bytes) -> bool:
        if not rendered_bytes or len(rendered_bytes) == 0:
            return False
        content = rendered_bytes.decode("utf-8", errors="ignore")
        return "# Digital Trust Report" in content and "## Risk Assessment" in content

    def get_content_type(self) -> str:
        return "text/markdown; charset=utf-8"

    def get_file_extension(self) -> str:
        return "md"

    def get_renderer_version(self) -> str:
        return self.VERSION
