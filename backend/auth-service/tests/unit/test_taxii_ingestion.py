"""Unit tests for TAXII Collection Handling (Phase 3.9 Part 1A.23)."""

import pytest
from app.schemas.threat_intelligence_models import TaxiiCollectionDTO


def test_taxii_collection_dto():
    tc = TaxiiCollectionDTO(
        collection_id="col_1",
        title="Malware Feeds Collection",
    )

    assert tc.collection_id == "col_1"
