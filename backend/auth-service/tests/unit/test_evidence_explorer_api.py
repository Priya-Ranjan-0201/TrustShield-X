"""Unit Tests — Evidence Explorer (Phase 4.0 Part 4 — Sections 10-12, 83)."""

import pytest
from app.schemas.digital_trust_report_models import ReportEvidenceCardDTO


class TestEvidenceExplorer:
    def test_evidence_card_dto_preserves_strength_and_confidence(self):
        ev = ReportEvidenceCardDTO(
            card_id="EV_01",
            category="STORAGE",
            title="SQLite Database File",
            observation="Observed plain database table 'tokens' in world-readable mode",
            evidence_strength="DIRECT",
            confidence="HIGH",
            source="DEX_PARSER",
            finding_reference="F_01",
        )
        assert ev.card_id == "EV_01"
        assert ev.evidence_strength == "DIRECT"
        assert ev.confidence == "HIGH"
        assert ev.finding_reference == "F_01"
