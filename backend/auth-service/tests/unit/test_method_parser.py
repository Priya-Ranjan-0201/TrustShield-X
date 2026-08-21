"""Unit tests for Method Structure Extraction (Phase 3.7 Part 1A.13)."""

import pytest
from app.schemas.dex_structure_models import MethodStructureDTO


def test_method_structure_dto():
    m = MethodStructureDTO(
        method_name="login",
        class_name="com.bank.auth.AuthManager",
        package_name="com.bank.auth",
        return_type="Z",
        parameter_types=["Ljava/lang/String;", "Ljava/lang/String;"],
        is_static=False,
        is_native=False,
        register_count=4,
        instruction_count=12,
    )

    assert m.method_name == "login"
    assert m.class_name == "com.bank.auth.AuthManager"
    assert m.package_name == "com.bank.auth"
    assert len(m.parameter_types) == 2
    assert m.register_count == 4
    assert m.instruction_count == 12
