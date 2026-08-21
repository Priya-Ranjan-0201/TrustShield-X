"""Unit tests for Package Tree Hierarchy Extraction (Phase 3.7 Part 1A.13)."""

import pytest
from app.schemas.dex_structure_models import PackageNodeDTO


def test_package_node_dto():
    pkg = PackageNodeDTO(
        package_name="com.bank.security",
        parent_package="com.bank",
        depth=3,
        class_count=14,
        method_count=88,
    )

    assert pkg.package_name == "com.bank.security"
    assert pkg.parent_package == "com.bank"
    assert pkg.depth == 3
    assert pkg.class_count == 14
    assert pkg.method_count == 88
