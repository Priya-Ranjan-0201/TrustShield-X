"""Unit tests for Cryptography Evidence Preservation (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEvidenceDTO


def test_crypto_evidence_dto():
    ev = CanonicalEvidenceDTO(
        evidence_id="ev_crypto_1",
        canonical_entity_id="entity_crypto_1",
        source_module="CRYPTOGRAPHY_INTELLIGENCE",
        evidence_type="CRYPTOGRAPHY",
        evidence_subtype="CIPHER_OPERATION",
        provenance_reference="Cipher.getInstance(AES/CBC/PKCS5Padding)",
    )

    assert ev.evidence_type == "CRYPTOGRAPHY"
