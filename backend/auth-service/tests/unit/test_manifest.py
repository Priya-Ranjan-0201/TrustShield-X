"""Unit Tests — Report Manifest (Phase 4.0 Part 3 — Section 40)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO
from app.schemas.report_rendering_models import ReportArtifactDTO


class TestReportManifest:
    """Section 40: Verify Report Manifest generation containing hashes and versions."""

    def test_report_manifest_generation(self):
        svc = ReportIntegrityService()
        ov = TrustOverviewDTO(risk_score=30.0, risk_band="LOW_RISK")
        doc = ReportDocumentDTO(report_id="rep_mf", analysis_id="an_mf", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        art = ReportArtifactDTO(
            artifact_id="art_mf",
            report_id="rep_mf",
            analysis_id="an_mf",
            format="JSON",
            mime_type="application/json",
            file_extension="json",
            sha256="abc123sha",
        )

        mf = svc.generate_manifest(doc, art)
        assert mf.report_id == "rep_mf"
        assert mf.artifact_id == "art_mf"
        assert mf.artifact_sha256 == "abc123sha"
        assert len(mf.content_sha256) == 64
        assert "risk_engine" in mf.engine_versions
