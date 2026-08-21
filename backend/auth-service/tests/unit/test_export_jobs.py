"""Unit Tests — Export Job Model & Management (Phase 4.0 Part 3 — Section 63)."""

import pytest
from app.services.report_rendering_orchestrator import ReportRenderingOrchestrator
from app.schemas.report_rendering_models import ReportExportJobDTO


class TestExportJobs:
    """Section 63: Test Report Export Job lifecycle and async status."""

    def test_create_export_job(self):
        orch = ReportRenderingOrchestrator()
        job = orch.create_export_job(report_id="rep_async_01", format_name="PDF", requested_by="analyst_1")
        assert isinstance(job, ReportExportJobDTO)
        assert job.report_id == "rep_async_01"
        assert job.format == "PDF"
        assert job.status in ("PENDING", "COMPLETED")
        assert job.progress == 100
