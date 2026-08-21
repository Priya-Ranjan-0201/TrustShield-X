"""Unit tests for Entity Canonicalization (Phase 3.9 Part 1A.25)."""

import pytest
from app.schemas.evidence_consolidation_models import CanonicalEntityDTO


def test_entity_canonical_dto():
    entity = CanonicalEntityDTO(
        entity_id="entity_domain_1",
        entity_type="DOMAIN",
        canonical_value="example.com",
        display_name="example.com",
    )

    assert entity.canonical_value == "example.com"
