"""Unit tests for Class Structure Extraction (Phase 3.7 Part 1A.13)."""

import pytest
from app.schemas.dex_structure_models import ClassStructureDTO


def test_class_structure_dto():
    c = ClassStructureDTO(
        full_name="com.bank.ui.MainActivity",
        simple_name="MainActivity",
        package_name="com.bank.ui",
        superclass="android.app.Activity",
        interfaces=["android.view.View.OnClickListener"],
        is_public=True,
        is_abstract=False,
    )

    assert c.full_name == "com.bank.ui.MainActivity"
    assert c.simple_name == "MainActivity"
    assert c.package_name == "com.bank.ui"
    assert c.superclass == "android.app.Activity"
    assert len(c.interfaces) == 1
    assert c.is_public is True
