"""Unit tests for Library Inventory DTOs (Phase 3.7 Part 1A.16)."""

import pytest
from app.schemas.api_intelligence_models import LibraryInventoryDTO


def test_library_inventory_dto():
    lib = LibraryInventoryDTO(library_name="Retrofit", version="2.9.0", package_prefix="retrofit2")

    assert lib.library_name == "Retrofit"
    assert lib.version == "2.9.0"
    assert lib.package_prefix == "retrofit2"
