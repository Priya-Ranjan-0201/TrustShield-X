"""HTML Report Renderer (Phase 4.0 Part 3 — Sections 10-28).

Generates standalone, responsive, print-friendly HTML reports with strict XSS escaping,
accessible semantic markup, and internal anchor navigation. Zero external dependencies.
"""

import html
from typing import Any, Optional, Dict
from app.schemas.digital_trust_report_models import ReportDocumentDTO
from app.schemas.trust_narrative_models import NarrativeDocumentDTO
from app.services.renderers.base_renderer import BaseReportRenderer


def _esc(val: Any) -> str:
    """Safely escape dynamic values for HTML embedding."""
    if val is None:
        return ""
    return html.escape(str(val))


class HTMLReportRenderer(BaseReportRenderer):
    """Production-grade HTML Report Renderer producing standalone self-contained HTML."""

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
        lang = report_doc.language or "en"
        watermark = (options or {}).get("watermark", "")

        # Determine theme colors based on risk band
        band_colors = {
            "TRUSTED": "#10b981",
            "LOW_RISK": "#06b6d4",
            "MODERATE_RISK": "#f59e0b",
            "HIGH_RISK": "#f97316",
            "CRITICAL_RISK": "#ef4444",
        }
        theme_color = band_colors.get(risk_band, "#8b5cf6")

        # HTML Head and Styles
        html_parts = [
            "<!DOCTYPE html>",
            f'<html lang="{_esc(lang)}">',
            "<head>",
            '<meta charset="UTF-8">',
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f'<title>Digital Trust Report — {_esc(report_doc.report_id)}</title>',
            "<style>",
            """
            :root {
                --primary: #4f46e5;
                --bg: #0f172a;
                --surface: #1e293b;
                --surface-card: #334155;
                --text: #f8fafc;
                --text-muted: #94a3b8;
                --border: #475569;
            }
            @media print {
                body { background: #fff !important; color: #000 !important; }
                .card { border: 1px solid #ccc !important; background: #fafafa !important; }
                .no-print { display: none !important; }
                .page-break { page-break-before: always; }
            }
            body {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 0;
                line-height: 1.6;
            }
            .container { max-width: 1000px; margin: 0 auto; padding: 2rem 1.5rem; }
            header { border-bottom: 2px solid var(--border); padding-bottom: 1.5rem; margin-bottom: 2rem; }
            .badge { display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-weight: 700; font-size: 0.85rem; }
            .card { background: var(--surface); border: 1px solid var(--border); border-radius: 0.75rem; padding: 1.5rem; margin-bottom: 1.5rem; }
            h1, h2, h3, h4 { color: #fff; margin-top: 0; }
            h1 { font-size: 2rem; }
            h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-top: 2rem; }
            h3 { font-size: 1.2rem; }
            table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.9rem; }
            th, td { text-align: left; padding: 0.75rem; border-bottom: 1px solid var(--border); }
            th { background: var(--surface-card); color: var(--text); }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
            .metric-box { background: var(--surface-card); padding: 1rem; border-radius: 0.5rem; text-align: center; }
            .metric-val { font-size: 1.8rem; font-weight: 800; }
            .metric-lbl { font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase; }
            .nav-anchors { display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 1rem 0; font-size: 0.85rem; }
            .nav-anchors a { color: #818cf8; text-decoration: none; padding: 0.25rem 0.5rem; background: var(--surface-card); border-radius: 0.25rem; }
            .nav-anchors a:hover { background: #4f46e5; color: #fff; }
            .watermark { text-align: center; color: #f59e0b; font-weight: bold; letter-spacing: 2px; margin-bottom: 1rem; }
            .limitation-item { color: #cbd5e1; margin-bottom: 0.5rem; }
            """,
            "</style>",
            "</head>",
            "<body>",
            '<div class="container">',
        ]

        if watermark:
            html_parts.append(f'<div class="watermark">*** {_esc(watermark.upper())} ***</div>')

        # Navigation Bar / Quick Links
        html_parts.extend([
            "<header>",
            "<div>",
            '<span class="badge" style="background:#4338ca; color:#e0e7ff;">TRUTHSHIELD X</span>',
            f'<h1>Digital Trust Report</h1>',
            f'<p style="color:var(--text-muted); margin:0;">Report ID: <code>{_esc(report_doc.report_id)}</code> | Analysis ID: <code>{_esc(report_doc.analysis_id)}</code> | Generated: {_esc(report_doc.generated_at)}</p>',
            "</div>",
            '<nav class="nav-anchors no-print">',
            '<a href="#executive-summary">Executive Summary</a>',
            '<a href="#trust-overview">Trust Overview</a>',
            '<a href="#major-findings">Findings</a>',
            '<a href="#evidence-cards">Evidence</a>',
            '<a href="#threat-intelligence">Threat Intel</a>',
            '<a href="#recommendations">Recommendations</a>',
            '<a href="#limitations">Limitations</a>',
            '<a href="#technical-details">Technical Details</a>',
            "</nav>",
            "</header>",
        ])

        # Executive Summary Section
        html_parts.append('<section id="executive-summary" class="card">')
        html_parts.append('<h2>Executive Summary</h2>')
        if narrative_doc and narrative_doc.executive_summary:
            es = narrative_doc.executive_summary
            html_parts.append(f'<h3>{_esc(es.headline)}</h3>')
            html_parts.append(f'<p>{_esc(es.overall_assessment)}</p>')
            html_parts.append(f'<p><strong>Recommended Action:</strong> {_esc(es.recommended_action)}</p>')
        else:
            html_parts.append(f'<p>The analysis concluded with risk band <strong>{_esc(risk_band)}</strong> and score <strong>{risk_score:.1f}/100</strong>.</p>')
        html_parts.append('</section>')

        # Trust Overview Metrics
        html_parts.append('<section id="trust-overview" class="card">')
        html_parts.append('<h2>Trust Overview & Risk Assessment</h2>')
        html_parts.append('<div class="grid">')
        html_parts.append(f'<div class="metric-box"><div class="metric-val" style="color:{theme_color};">{risk_score:.1f}</div><div class="metric-lbl">Risk Score</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val" style="color:{theme_color}; font-size:1.2rem;">{_esc(risk_band)}</div><div class="metric-lbl">Risk Band</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val" style="font-size:1.2rem;">{_esc(confidence)}</div><div class="metric-lbl">Confidence</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val" style="font-size:1.2rem;">{_esc(sufficiency)}</div><div class="metric-lbl">Evidence Sufficiency</div></div>')
        html_parts.append('</div>')

        html_parts.append('<div class="grid" style="margin-top:1rem;">')
        html_parts.append(f'<div class="metric-box"><div class="metric-val">{ov.findings_count}</div><div class="metric-lbl">Findings Count</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val">{ov.evidence_count}</div><div class="metric-lbl">Evidence Records</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val">{ov.threat_matches}</div><div class="metric-lbl">Threat Matches</div></div>')
        html_parts.append(f'<div class="metric-box"><div class="metric-val">{ov.contradictions}</div><div class="metric-lbl">Contradictions</div></div>')
        html_parts.append('</div>')
        html_parts.append('</section>')

        # Major Findings Section with Anchors
        html_parts.append('<section id="major-findings" class="card">')
        html_parts.append('<h2>Major Findings</h2>')
        if report_doc.major_findings:
            for f in report_doc.major_findings:
                fid = _esc(f.finding_id)
                html_parts.append(f'<article id="finding-{fid}" class="card" style="background:var(--surface-card); margin-bottom:1rem;">')
                html_parts.append(f'<h3>Finding [{fid}]: {_esc(f.title)}</h3>')
                html_parts.append(f'<p><strong>Category:</strong> {_esc(f.category)} | <strong>Confidence:</strong> {_esc(f.confidence)} | <strong>Strength:</strong> {_esc(f.evidence_strength)}</p>')
                html_parts.append(f'<p>{_esc(f.description)}</p>')
                if f.source_modules:
                    html_parts.append(f'<p style="font-size:0.85rem; color:var(--text-muted);">Source Modules: {_esc(", ".join(f.source_modules))}</p>')
                if f.provenance_reference:
                    html_parts.append(f'<p style="font-size:0.85rem;"><a href="#provenance-{_esc(f.provenance_reference)}" style="color:#a5b4fc;">View Provenance &rarr;</a></p>')
                html_parts.append('</article>')
        else:
            html_parts.append('<p style="color:var(--text-muted);">No significant security findings were identified within the analyzed scope.</p>')
        html_parts.append('</section>')

        # Evidence Cards Section
        html_parts.append('<section id="evidence-cards" class="card">')
        html_parts.append('<h2>Evidence Cards</h2>')
        if report_doc.evidence_cards:
            for ev in report_doc.evidence_cards:
                cid = _esc(ev.card_id)
                html_parts.append(f'<article id="evidence-{cid}" class="card" style="background:var(--surface-card); margin-bottom:1rem;">')
                html_parts.append(f'<h4>Evidence [{cid}]: {_esc(ev.title)}</h4>')
                html_parts.append(f'<p><strong>Category:</strong> {_esc(ev.category)} | <strong>Strength:</strong> {_esc(ev.evidence_strength)} | <strong>Source:</strong> {_esc(ev.source)}</p>')
                html_parts.append(f'<p>{_esc(ev.observation)}</p>')
                if ev.limitations:
                    html_parts.append(f'<p style="font-size:0.85rem; color:#fca5a5;">Limitations: {_esc("; ".join(ev.limitations))}</p>')
                html_parts.append('</article>')
        else:
            html_parts.append('<p style="color:var(--text-muted);">No supporting evidence cards present.</p>')
        html_parts.append('</section>')

        # Threat Intelligence Table
        html_parts.append('<section id="threat-intelligence" class="card">')
        html_parts.append('<h2>Threat Intelligence Correlation</h2>')
        if report_doc.threat_intelligence:
            html_parts.append('<table>')
            html_parts.append('<thead><tr><th>Indicator</th><th>Type</th><th>Provider</th><th>Confidence</th><th>Freshness</th></tr></thead>')
            html_parts.append('<tbody>')
            for ti in report_doc.threat_intelligence:
                html_parts.append('<tr>')
                html_parts.append(f'<td><code>{_esc(ti.get("indicator", "N/A"))}</code></td>')
                html_parts.append(f'<td>{_esc(ti.get("type", ti.get("ioc_type", "N/A")))}</td>')
                html_parts.append(f'<td>{_esc(ti.get("provider", "Internal Catalog"))}</td>')
                html_parts.append(f'<td>{_esc(ti.get("confidence", "HIGH"))}</td>')
                html_parts.append(f'<td>{_esc(ti.get("freshness", "CURRENT"))}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody></table>')
        else:
            html_parts.append('<p style="color:var(--text-muted);">No threat intelligence matches observed.</p>')
        html_parts.append('</section>')

        # Recommendations Section
        html_parts.append('<section id="recommendations" class="card">')
        html_parts.append('<h2>Recommendations</h2>')
        if report_doc.recommendations:
            html_parts.append('<ol>')
            for rec in report_doc.recommendations:
                html_parts.append(f'<li>{_esc(rec)}</li>')
            html_parts.append('</ol>')
        else:
            html_parts.append('<p style="color:var(--text-muted);">No specific actions required at this time.</p>')
        html_parts.append('</section>')

        # Contradictions Section (if any)
        if report_doc.contradictions:
            html_parts.append('<section id="contradictions" class="card" style="border-color:#f59e0b;">')
            html_parts.append('<h2 style="color:#f59e0b;">Contradictory Evidence & Conflicts</h2>')
            for c in report_doc.contradictions:
                html_parts.append(f'<div class="card" style="background:#451a03; border-color:#b45309;">')
                html_parts.append(f'<h4>Conflict [{_esc(c.contradiction_id)}]</h4>')
                html_parts.append(f'<p><strong>Evidence A ({_esc(c.source_a)}):</strong> {_esc(c.evidence_a)}</p>')
                html_parts.append(f'<p><strong>Evidence B ({_esc(c.source_b)}):</strong> {_esc(c.evidence_b)}</p>')
                html_parts.append(f'<p><strong>Explanation:</strong> {_esc(c.explanation)}</p>')
                html_parts.append('</div>')
            html_parts.append('</section>')

        # Limitations Section
        html_parts.append('<section id="limitations" class="card">')
        html_parts.append('<h2>Analysis Limitations & Scope</h2>')
        if report_doc.limitations:
            html_parts.append('<ul>')
            for lim in report_doc.limitations:
                html_parts.append(f'<li class="limitation-item">{_esc(lim)}</li>')
            html_parts.append('</ul>')
        else:
            html_parts.append('<p>Standard static analysis limitations apply.</p>')
        html_parts.append('</section>')

        # Technical Details & Provenance Section
        html_parts.append('<section id="technical-details" class="card">')
        html_parts.append('<h2>Technical Details & Lineage</h2>')
        html_parts.append(f'<p><strong>Schema Version:</strong> {_esc(report_doc.schema_version)} | <strong>Report Version:</strong> {_esc(report_doc.report_version)}</p>')
        html_parts.append(f'<p><strong>Generated By:</strong> {_esc(report_doc.generated_by)}</p>')
        if report_doc.provenance:
            html_parts.append('<h3>Provenance Records</h3>')
            html_parts.append('<table>')
            html_parts.append('<thead><tr><th>Statement ID</th><th>Source Module</th><th>Finding ID</th><th>Evidence ID</th><th>Timestamp</th></tr></thead>')
            html_parts.append('<tbody>')
            for p in report_doc.provenance:
                html_parts.append(f'<tr id="provenance-{_esc(p.statement_id)}">')
                html_parts.append(f'<td><code>{_esc(p.statement_id)}</code></td>')
                html_parts.append(f'<td>{_esc(p.source_module)}</td>')
                html_parts.append(f'<td>{_esc(p.finding_id)}</td>')
                html_parts.append(f'<td>{_esc(p.evidence_id)}</td>')
                html_parts.append(f'<td>{_esc(p.timestamp)}</td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody></table>')
        html_parts.append('</section>')

        # Footer
        html_parts.extend([
            "<footer>",
            f'<p style="text-align:center; color:var(--text-muted); font-size:0.8rem; margin-top:2rem;">TruthShield X &bull; Digital Trust Report &bull; Cryptographically Verifiable</p>',
            "</footer>",
            "</div>",
            "</body>",
            "</html>",
        ])

        return "\n".join(html_parts).encode("utf-8")

    def validate_output(self, rendered_bytes: bytes) -> bool:
        if not rendered_bytes or len(rendered_bytes) == 0:
            return False
        content = rendered_bytes.decode("utf-8", errors="ignore")
        return "<!DOCTYPE html>" in content and "</html>" in content

    def get_content_type(self) -> str:
        return "text/html; charset=utf-8"

    def get_file_extension(self) -> str:
        return "html"

    def get_renderer_version(self) -> str:
        return self.VERSION
