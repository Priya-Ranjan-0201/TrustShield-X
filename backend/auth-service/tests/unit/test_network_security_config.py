"""Unit tests for Network Security Configuration Analysis (Phase 3.8 Part 1A.19)."""

import pytest
from app.schemas.network_models import NetworkEvidenceDTO


def test_network_security_config_evidence():
    ev = NetworkEvidenceDTO(
        dex_id="res/xml/network_security_config.xml",
        class_name="Manifest",
        method_name="networkSecurityConfig",
        instruction_offset=0,
        evidence_type="CLEAR_TEXT_PERMITTED",
        raw_evidence="cleartextTrafficPermitted=false",
    )

    assert ev.evidence_type == "CLEAR_TEXT_PERMITTED"
    assert "cleartextTrafficPermitted" in ev.raw_evidence
