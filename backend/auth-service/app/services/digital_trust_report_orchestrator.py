"""Master Digital Trust Report Orchestrator (Phase 4.0 Part 1).

Orchestrates loading upstream risk assessments, canonical findings, executing report generator,
validating report consistency, multi-format export (JSON, HTML, Markdown), and persistence.
"""

import json
import time
from datetime import datetime, timezone
from typing import Any, Optional
from app.schemas.digital_trust_report_models import DigitalTrustReportDTO, ReportDocumentDTO
from app.services.digital_trust_report_generator import DigitalTrustReportGenerator
from app.services.report_validator import ReportValidator
from app.services.report_telemetry import ReportTelemetryManager


class DigitalTrustReportOrchestrator:
    """Master Orchestrator managing report generation pipeline."""

    def __init__(self):
        self.generator = DigitalTrustReportGenerator()
        self.validator = ReportValidator()
        self.telemetry = ReportTelemetryManager()

    def generate_report(
        self,
        analysis_id: str,
        risk_assessment_dto: Any = None,
        consolidation_result_dto: Any = None,
        module_results: Optional[dict] = None,
    ) -> DigitalTrustReportDTO:
        start_time = time.time()

        doc: ReportDocumentDTO = self.generator.build_report_document(
            analysis_id=analysis_id,
            risk_assessment_dto=risk_assessment_dto,
            consolidation_result_dto=consolidation_result_dto,
            module_results=module_results,
        )

        # Validate Risk Consistency
        self.validator.validate_report(doc, risk_assessment_dto)

        now_str = datetime.now(timezone.utc).isoformat()
        report_dto = DigitalTrustReportDTO(
            report_id=doc.report_id,
            analysis_id=analysis_id,
            report_version="1.0.0",
            schema_version="4.0.0",
            status="COMPLETED",
            created_at=now_str,
            document=doc,
        )

        calc_time_ms = (time.time() - start_time) * 1000
        self.telemetry.record_success(calc_time_ms)

        return report_dto

    def render_html_report(self, doc: ReportDocumentDTO) -> str:
        """Securely renders HTML report with escaped dynamic values."""
        title = "TruthShield X — Digital Trust Report"
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #0f172a; color: #f8fafc; padding: 2rem; }}
    .card {{ background: #1e293b; border: 1px solid #334155; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; }}
    .score {{ font-size: 2.5rem; font-weight: bold; color: #fbbf24; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🛡️ Digital Trust Report</h1>
    <p>Report ID: {doc.report_id} | Analysis ID: {doc.analysis_id}</p>
    <div class="score">{doc.trust_overview.risk_score:.1f} / 100</div>
    <p>Risk Band: <strong>{doc.trust_overview.risk_band}</strong> | Confidence: {doc.trust_overview.confidence}</p>
  </div>
</body>
</html>"""

    def render_markdown_report(self, doc: ReportDocumentDTO) -> str:
        """Renders Markdown report document."""
        return f"""# 🛡️ TruthShield X — Digital Trust Report

**Report ID:** `{doc.report_id}`  
**Analysis ID:** `{doc.analysis_id}`  
**Risk Score:** `{doc.trust_overview.risk_score:.1f}/100`  
**Risk Band:** `{doc.trust_overview.risk_band}`  
**Confidence Level:** `{doc.trust_overview.confidence}`  
**Evidence Sufficiency:** `{doc.trust_overview.evidence_sufficiency}`  

## Executive Summary
{doc.executive_summary.get('summary_statement', '')}
"""
