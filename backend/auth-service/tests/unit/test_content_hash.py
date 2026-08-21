"""Unit Tests — Canonical Content Hash (Phase 4.0 Part 3 — Section 84, Tests 8, 10, 11)."""

import pytest
from app.services.report_integrity_service import ReportIntegrityService
from app.schemas.digital_trust_report_models import ReportDocumentDTO, TrustOverviewDTO, ReportFindingDTO


class TestCanonicalContentHash:
    """Mandatory Tests 8, 10, 11: Canonical content hash determinism and change sensitivity."""

    def test_same_report_same_content_hash(self):
        svc = ReportIntegrityService()
        ov = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        doc1 = ReportDocumentDTO(report_id="rep_1", analysis_id="an_1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)
        doc2 = ReportDocumentDTO(report_id="rep_1", analysis_id="an_1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov)

        hash1 = svc.calculate_canonical_content_hash(doc1)
        hash2 = svc.calculate_canonical_content_hash(doc2)
        assert hash1 == hash2

    def test_modified_report_content_changes_hash(self):
        svc = ReportIntegrityService()
        ov1 = TrustOverviewDTO(risk_score=50.0, risk_band="MODERATE_RISK")
        ov2 = TrustOverviewDTO(risk_score=55.0, risk_band="MODERATE_RISK")
        doc1 = ReportDocumentDTO(report_id="rep_1", analysis_id="an_1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov1)
        doc2 = ReportDocumentDTO(report_id="rep_1", analysis_id="an_1", generated_at="2026-08-14T00:00:00Z", trust_overview=ov2)

        hash1 = svc.calculate_canonical_content_hash(doc1)
        hash2 = svc.calculate_canonical_content_hash(doc2)
        assert hash1 != hash2
