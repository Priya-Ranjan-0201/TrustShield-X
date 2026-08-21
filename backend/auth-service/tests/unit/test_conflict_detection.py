"""Unit tests for Contradiction & Conflict Detection (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import FindingConflictDTO


def test_finding_conflict_dto():
    conflict = FindingConflictDTO(
        conflict_id="cfl_1",
        finding_id="f_crypto",
        evidence_a_id="ev_plain",
        evidence_b_id="ev_cipher",
        conflict_type="PLAINTEXT_VS_ENCRYPTED",
        explanation="Branch A uses HTTP cleartext while Branch B uses TLS HTTPS",
    )

    assert conflict.conflict_type == "PLAINTEXT_VS_ENCRYPTED"
