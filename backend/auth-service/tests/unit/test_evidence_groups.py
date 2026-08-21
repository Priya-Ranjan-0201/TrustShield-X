"""Unit tests for Evidence Group Classification (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import EvidenceGroupDTO


def test_evidence_group_dto():
    grp = EvidenceGroupDTO(
        group_id="group_net",
        group_name="NETWORK_GROUP",
        member_evidence_count=3,
    )

    assert grp.group_name == "NETWORK_GROUP"
    assert grp.member_evidence_count == 3
