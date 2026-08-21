"""Unit tests for Evidence Identity Fingerprinting (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_evidence_identity_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="fingerprint_hash_1",
        canonical_entity_id="entity_1",
        source_module="API_INTELLIGENCE",
        evidence_type="API",
        provenance_reference="SmsManager.sendTextMessage",
    )

    assert ev.evidence_id == "fingerprint_hash_1"
