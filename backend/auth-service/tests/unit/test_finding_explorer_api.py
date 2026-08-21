"""Unit Tests — Finding Explorer (Phase 4.0 Part 4 — Sections 7-9, 83)."""

import pytest
from app.schemas.digital_trust_report_models import ReportFindingDTO


class TestFindingExplorer:
    def test_finding_dto_preserves_severity_and_contribution(self):
        f = ReportFindingDTO(
            finding_id="F_01",
            category="STORAGE",
            severity_reference="CRITICAL",
            title="Plaintext Credentials",
            description="Stored in SQLite without encryption",
            confidence="HIGH",
        )
        assert f.finding_id == "F_01"
        assert f.severity_reference == "CRITICAL"
        assert f.confidence == "HIGH"
